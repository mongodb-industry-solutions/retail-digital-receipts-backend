# app/infrastructure/vector_search/mongodb_vector_search_adapter.py

"""
Adapter – MongoDB Vector Search Implementation

This class implements the VectorSearchPort interface using MongoDB Atlas Vector Search.
It performs the $vectorSearch aggregation against the 'products' collection and maps
the results into domain-level RecommendationItem objects.
"""

import logging
from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.models.recommendation_item import RecommendationItem
from app.infrastructure.db.mongo_client import get_db
from app.infrastructure.vector_search.vector_search_mapper import map_vector_search_result
from app.infrastructure.config.settings import settings

logger = logging.getLogger(__name__)

class MongoDBVectorSearchAdapter(VectorSearchPort):
    """
    VectorSearchPort implementation using MongoDB Atlas Vector Search.
    """

    def __init__(self):
        # get_db() already returns the correct Database instance (settings.database_name)
        self.db = get_db()
        # collection name is fixed
        self.collection = self.db["products"]
        self.index_name = settings.vector_index_name
        self.embedding_field = settings.embedding_field

        logger.info(
            "MongoDBVectorSearchAdapter initialized (index=%s, field=%s)",
            self.index_name,
            self.embedding_field
        )

    async def find_similar_products(self, embedding: list[float], limit: int = 4) -> list[RecommendationItem]:
        """
        Perform a vector similarity search using a single product embedding.

        Args:
            embedding (list[float]): The embedding vector of the anchor product.
            limit (int): Number of similar products to return.

        Returns:
            list[RecommendationItem]: Top similar products.
        """
        logger.info("Running vector search with embedding of length %d", len(embedding))

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
