"""
Use Case – Generate Recommendation

Triggered by a new invoice insert:
  • Extract the most expensive product
  • Lookup its embedding vector
  • Run vector search to find similar products
  • Filter out duplicates by name
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

    def _filter_similar_items(self, items: List[RecommendationItem], max_items: int) -> List[RecommendationItem]:
        """
        Removes duplicates based on normalized product names (case-insensitive).
        Useful for avoiding near-duplicate items differing only in price or metadata.

        Args:
            items (List[RecommendationItem]): Raw results from vector search.
            max_items (int): Max number of items to return.

        Returns:
            List[RecommendationItem]: Filtered list of unique products.
        """
        filtered = []
        seen_names = set()

        for item in items:
            name_key = item.name.strip().lower()
            if name_key in seen_names:
                logger.debug("Duplicate product name detected: %s", item.name)
                continue

            seen_names.add(name_key)
            filtered.append(item)

            if len(filtered) == max_items:
                break

        return filtered

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
        raw_items: List[RecommendationItem] = await self.vector_search.find_similar_products(embedding)
        logger.info("Vector search returned %d raw items for invoice %s", len(raw_items), invoice_id)

        # Step 3.1 – filter to remove duplicates
        filtered_items = self._filter_similar_items(raw_items, max_items=4)
        logger.info("Filtered recommendation list to %d unique items", len(filtered_items))

        # Step 4 – build and save the RecommendationGroup
        recommendation_group = RecommendationGroup(
            user_id=invoice["userId"],
            invoice_id=invoice_id,
            created_at=datetime.utcnow(),
            items=filtered_items,
        )

        inserted_id = await self.repository.save(recommendation_group)
        logger.info(
            "Recommendation saved with ID: %s for invoice %s",
            inserted_id, invoice_id
        )
        return True
