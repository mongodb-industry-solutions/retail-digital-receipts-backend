# app/application/use_cases/generate_recommendation.py

"""
Use Case – Generate Recommendation

Triggered by a new invoice insert:
  • Extract the most expensive product
  • Run vector search to find similar products
  • Wrap results in a RecommendationGroup
  • Persist via the repository
"""

import logging
from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.repositories.recommendation_repository import RecommendationRepository
from app.domain.models.recommendation_group import RecommendationGroup
from app.domain.models.recommendation_item import RecommendationItem
from datetime import datetime

logger = logging.getLogger(__name__)

class GenerateRecommendation:
    def __init__(self, vector_search: VectorSearchPort, repository: RecommendationRepository):
        self.vector_search = vector_search
        self.repository = repository

    async def execute(self, invoice: dict):
        """
        Main method to generate and persist a product recommendation based on the invoice.

        Args:
            invoice (dict): The full invoice document received via Change Stream.
        """
        invoice_id = invoice.get("_id")
        logger.info("Generating recommendation for invoice: %s", invoice_id)

        # Step 1: Extract the most expensive product
        products = invoice.get("products", [])
        if not products:
            logger.warning("Invoice has no products, skipping.")
            return

        most_expensive = max(products, key=lambda p: p.get("price", 0))
        embedding = most_expensive.get("embedding")

        if not embedding:
            logger.warning("No embedding found in most expensive product: %s", most_expensive)
            return

        # Step 2: Perform vector search
        similar_items: list[RecommendationItem] = await self.vector_search.find_similar_products(embedding)

        # Step 3: Build and save the RecommendationGroup
        recommendation_group = RecommendationGroup(
            user_id=invoice["userId"],
            invoice_id=str(invoice_id),
            created_at=datetime.utcnow(),
            items=similar_items
        )

        inserted_id = await self.repository.save(recommendation_group)
        logger.info("Recommendation saved with ID: %s", inserted_id)
# ---
        # Example of the saved document in MongoDB (recommendations collection):
        #
        # {
        #   "_id": "6628446b2717e12b0f4fa8c1",
        #   "userId": "user_123",
        #   "invoiceId": "invoice_456",
        #   "createdAt": "2025-04-24T15:33:00.000Z",
        #   "recommendations": [
        #     {
        #       "productId": "67192b3f64d161905fbe7790",
        #       "name": "Amazon Brand - Solimo Designer Never Stop Dreaming 3D Printed Hard Back Case",
        #       "brand": "Amazon Brand - Solimo",
        #       "price": 97,
        #       "image": "https://m.media-amazon.com/images/I/71W6WJAQ5pL.jpg",
        #       "vectorSearchScore": 2.435
        #     },
        #     {
        #       "productId": "67020a3f64d161905fbe7133",
        #       "name": "Boat Rockerz 255 Pro+ Wireless Earphones",
        #       "brand": "boAt",
        #       "price": 999,
        #       "image": "https://m.media-amazon.com/images/I/61B04f0ALWL._SX679_.jpg",
        #       "vectorSearchScore": 2.129
        #     },
        #     {
        #       "productId": "66ff3c1a6b00c58df7ee1122",
        #       "name": "OnePlus Nord Buds 2",
        #       "brand": "OnePlus",
        #       "price": 1999,
        #       "image": "https://m.media-amazon.com/images/I/618E0d0v8GL._SX679_.jpg",
        #       "vectorSearchScore": 1.986
        #     },
        #     {
        #       "productId": "66ea3f4f92713ef990abc3de",
        #       "name": "Realme Buds Wireless 2 Neo",
        #       "brand": "realme",
        #       "price": 1299,
        #       "image": "https://m.media-amazon.com/images/I/51R5YBJdMCL._SX679_.jpg",
        #       "vectorSearchScore": 1.913
        #     }
        #   ]
        # }
        # ---
