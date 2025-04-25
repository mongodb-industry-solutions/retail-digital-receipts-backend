# app/domain/ports/vector_search_port.py

"""
Port (Interface) – Clean Architecture Principle

This file defines WHAT the application needs, not HOW it is done.

The Recommendation use case needs to:
  • Find similar products using an embedding vector.
  • Retrieve the embedding vector for a specific product ID.

This interface defines these needs without depending on the actual implementation
(MongoDB, external API, mock, etc.). It allows fetching embedding vectors directly
from products, supporting operations that require vector-based product comparisons.

By using a Port, we decouple our domain from infrastructure and make it easier
to test, replace, or evolve the logic in the future.
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models.recommendation_item import RecommendationItem

class VectorSearchPort(ABC):
    @abstractmethod
    async def find_similar_products(self, embedding: List[float], limit: int = 4) -> List[RecommendationItem]:
        """Return top N similar products given an embedding."""

    @abstractmethod
    async def get_embedding(self, product_id: str) -> Optional[List[float]]:
        """
        Lookup and return the raw embedding vector for a given product ID.
        Returns None if not found.
        """
