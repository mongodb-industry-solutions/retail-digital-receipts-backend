# app/infrastructure/vector_search/mongodb_vector_search_adapter.py

"""
Adapter – MongoDB Vector Search + Embedding Lookup

This class implements the VectorSearchPort interface using MongoDB Atlas Vector Search
and also provides a lookup method to retrieve a product’s raw embedding vector
from the `products` collection.
"""

import logging
from bson import ObjectId
from typing import List, Optional, Union

from motor.motor_asyncio import AsyncIOMotorDatabase

from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.models.recommendation_item import RecommendationItem
from app.infrastructure.db.mongo_client import get_db
from app.infrastructure.vector_search.vector_search_mapper import map_vector_search_result
from app.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)

class MongoDBVectorSearchAdapter(VectorSearchPort):
    """
    VectorSearchPort implementation that combines:
      1) A method to fetch the raw embedding for a given product ID.
      2) A method to perform $vectorSearch on those embeddings.
    """

    def __init__(self):
        # Acquire the singleton Database instance
        self.db: AsyncIOMotorDatabase = get_db()
        self.collection = self.db["products"]
        self.index_name = settings.vector_index_name
        self.embedding_field = settings.embedding_field

        logger.info(
            "MongoDBVectorSearchAdapter initialized (index=%s, field=%s)",
            self.index_name, self.embedding_field
        )

    async def get_embedding(
        self,
        product_id: Union[str, ObjectId]
    ) -> Optional[List[float]]:
        """
        Lookup and return the raw embedding vector for a given product ID.
        Accepts either an ObjectId or its string representation. Returns None
        if the product is not found or has no embedding.
        """
        # Normalize to ObjectId
        if not isinstance(product_id, ObjectId):
            try:
                product_id = ObjectId(product_id)
            except Exception:
                logger.error("Invalid product ID format: %s", product_id)
                return None

        logger.info("Looking up embedding for product ID %s", product_id)
        try:
            doc = await self.collection.find_one(
                {"_id": product_id},
                {self.embedding_field: 1}
            )
        except Exception as e:
            logger.error("Error fetching embedding for %s: %s", product_id, e)
            return None

        if not doc or self.embedding_field not in doc:
            logger.warning("No embedding found for product %s", product_id)
            return None

        embedding = doc[self.embedding_field]
        logger.info(
            "Fetched embedding for %s (length=%d)",
            product_id, len(embedding) if isinstance(embedding, list) else 0
        )
        return embedding

    async def find_similar_products(
        self,
        embedding: List[float],
        limit: int = 100 #we limit until 100 because we are going to filter them to the most relevant by applying some filter logic
    ) -> List[RecommendationItem]:
        """
        Perform a vector similarity search using a single product embedding.

        Args:
            embedding (list[float]): The embedding vector of the anchor product.
            limit (int): Number of similar products to return.

        Returns:
            list[RecommendationItem]: Top similar products.
        """
        logger.info("Running vector search with embedding length %d", len(embedding))

        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,
                    "path": self.embedding_field,
                    "queryVector": embedding,
                    "numCandidates": 100,
                    "limit": limit
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "productId": "$_id",
                    "name": 1,
                    "brand": 1,
                    "price": 1,
                    "image": 1,
                    "vectorSearchScore": {"$meta": "vectorSearchScore"}
                }
            }
        ]

        logger.info("Executing $vectorSearch pipeline (limit=%d)...", limit)
        cursor = self.collection.aggregate(pipeline)

        results = [map_vector_search_result(doc) async for doc in cursor]

        logger.info("Vector search returned %d results", len(results))
        return results
