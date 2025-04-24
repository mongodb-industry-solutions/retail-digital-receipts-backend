# app/domain/ports/vector_search_port.py

"""
Port (Interface) – Clean Architecture Principle

This file defines WHAT the application needs, not HOW it is done.

The Recommendation use case needs to find similar products using an embedding.
This interface defines that need, without depending on the actual implementation
(MongoDB, external API, mock, etc.).

By using a Port, we decouple our domain from infrastructure and make it easier
to test, replace, or evolve the logic in the future.
"""

from abc import ABC, abstractmethod
from typing import List
from app.domain.models.recommendation_item import RecommendationItem

class VectorSearchPort(ABC):
    @abstractmethod
    async def find_similar_products(self, embedding: List[float], limit: int = 4) -> List[RecommendationItem]:
        """Return top N similar products given an embedding."""
        pass
