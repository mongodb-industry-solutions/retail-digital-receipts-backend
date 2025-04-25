# app/application/use_cases/generate_recommendation.py

"""
Use Case – Generate Recommendation

Triggered by a new invoice insert:
  • Extract the most expensive product
  • Lookup its embedding vector
  • Run vector search to find similar products
  • Wrap results in a RecommendationGroup
  • Persist via the repository
"""

import logging
from datetime import datetime
from typing import List, Optional

from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.repositories.recommendation_repository import RecommendationRepository
from app.domain.models.recommendation_group import RecommendationGroup
from app.domain.models.recommendation_item import RecommendationItem

logger = logging.getLogger(__name__)


class GenerateRecommendation:
    def __init__(self, vector_search: VectorSearchPort, repository: RecommendationRepository):
        self.vector_search = vector_search
        self.repository = repository

    async def execute(self, invoice: dict) -> bool:
        """
        Main method to generate and persist a product recommendation based on the invoice.

        Args:
            invoice (dict): The full invoice document received via Change Stream.

        Returns:
            bool: True if a recommendation was generated and saved, False otherwise.
        """
        invoice_id = invoice.get("_id")
        logger.info("Generating recommendation for invoice: %s", invoice_id)

        # Step 1 – extract the most-expensive product
        items = invoice.get("items") or invoice.get("products", [])
        if not items:
            logger.warning("Invoice %s has no products, skipping.", invoice_id)
            return False

        most_expensive = max(
            items,
            key=lambda p: p.get("price", {}).get("amount", 0)
        )
        product_id = most_expensive.get("_id")
        logger.info("Most expensive product ID: %s", product_id)

        # Step 2 – lookup the embedding for the product
        logger.info("Looking up embedding for product %s", product_id)
        embedding = await self.vector_search.get_embedding(product_id)
        if not embedding:
            logger.warning(
                "No embedding found for product %s in invoice %s, skipping.",
                product_id, invoice_id
            )
            return False
        logger.info(
            "Fetched embedding for product %s (length=%d)",
            product_id, len(embedding)
        )

        # Step 3 – perform vector search
        similar_items: List[RecommendationItem] = await self.vector_search.find_similar_products(embedding)
        logger.info(
            "Vector search returned %d items for invoice %s",
            len(similar_items), invoice_id
        )

        # Step 4 – build and save the RecommendationGroup
        recommendation_group = RecommendationGroup(
            user_id=invoice["userId"],
            invoice_id=invoice_id,
            created_at=datetime.utcnow(),
            items=similar_items,
        )

        inserted_id = await self.repository.save(recommendation_group)
        logger.info(
            "Recommendation saved with ID: %s for invoice %s",
            inserted_id, invoice_id
        )
        return True


# ----------------------------------------------------------------------
# Example document stored in the `recommendations` collection
#
# {
#   "_id": "6628446b2717e12b0f4fa8c1",
#   "userId": "user_123",
#   "invoiceId": "invoice_456",
#   "createdAt": "2025-04-24T15:33:00.000Z",
#   "items": [
#     {
#       "productId": "67192b3f64d161905fbe7790",
#       "name": "Amazon Brand - Solimo Designer Never Stop Dreaming 3D Printed Hard Back Case",
#       "brand": "Amazon Brand - Solimo",
#       "price": 97,
#       "image": "https://m.media-amazon.com/images/I/71W6WJAQ5pL.jpg",
#       "vectorSearchScore": 2.435
#     },
#     ...
#   ]
# }
# ----------------------------------------------------------------------
