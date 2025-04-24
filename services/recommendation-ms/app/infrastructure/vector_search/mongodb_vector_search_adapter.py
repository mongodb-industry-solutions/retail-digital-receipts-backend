# app/infrastructure/vector_search/mongodb_vector_search_adapter.py

"""
Adapter – MongoDB Vector Search Implementation

This class implements the VectorSearchPort interface using MongoDB Atlas Vector Search.
It performs the $vectorSearch query against the 'products' collection and maps the results
into domain-level RecommendationItem objects.

The adapter is read-only and isolated from business logic. It can be replaced later with an
HTTP client or another backend without changing the rest of the application.
"""

import logging
from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.models.recommendation_item import RecommendationItem
from app.infrastructure.db.mongo_client import get_db
from app.infrastructure.utils.map_vs_result import map_vs_result
from app.core.settings import settings  # Adjust this path if needed

logger = logging.getLogger(__name__)

class MongoDBVectorSearchAdapter(VectorSearchPort):
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["products"]
        self.index_name = settings.vector_index_name
        self.embedding_field = settings.embedding_field

    async def find_similar_products(self, embedding: list[float], limit: int = 4) -> list[RecommendationItem]:
        """
        Perform a vector similarity search using a single product embedding.

        Args:
            embedding (list[float]): The embedding vector of the anchor product.
            limit (int): The number of similar products to return.

        Returns:
            list[RecommendationItem]: A list of the top similar products.
        """
        logger.info("Running vector search with embedding of length %d", len(embedding))

        pipeline = [
            {
                "$vectorSearch": {
                    "index": self.index_name,          # Comes from .env (VECTOR_INDEX_NAME)
                    "path": self.embedding_field,      # Comes from .env (EMBEDDING_FIELD)
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

        results = [map_vs_result(doc) async for doc in cursor]

        logger.info("Vector search returned %d results", len(results))
        return results
