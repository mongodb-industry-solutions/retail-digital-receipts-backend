"""Domain - Repository Port for Recommendations."""

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.models.recommendation_group import RecommendationGroup


class RecommendationRepository(ABC):
    """
    Port that isolates the application layer from the persistence layer.

    • Keeps business logic agnostic of MongoDB (or any other store).  
    • Works with the *domain* model `RecommendationGroup`.  
    """

    # --------------------------------------------------------------- #
    # Writes                                                          #
    # --------------------------------------------------------------- #
    @abstractmethod
    async def save(self, group: RecommendationGroup) -> str:
        """
        Persist a new RecommendationGroup.

        Returns the inserted document ID as a string.
        """
        raise NotImplementedError

    # --------------------------------------------------------------- #
    # Reads                                                           #
    # --------------------------------------------------------------- #
    @abstractmethod
    async def find_by_invoice_id(self, invoice_id: str) -> Optional[RecommendationGroup]:
        """
        Retrieve the recommendations linked to a given invoice.

        Returns None if no document is found.
        """
        raise NotImplementedError
