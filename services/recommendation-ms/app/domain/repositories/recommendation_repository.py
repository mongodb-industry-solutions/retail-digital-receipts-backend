from app.domain.models.recommendation import Recommendation
from abc import ABC, abstractmethod

class RecommendationRepository(ABC):
    """
    The RecommendationRepository interface defines the methods needed to interact with the persistence layer for recommendations.
    
    The purpose of this interface is to decouple the business logic from the specific infrastructure being used 
    (e.g., MongoDB). This allows for flexibility in changing the database or storage solution without affecting the core application.
    
    Methods:
        save(recommendation: Recommendation) -> str: Saves a recommendation to the database.
        find_by_invoice_id(invoice_id: str) -> Recommendation: Retrieves a recommendation by its associated invoice ID.
    """
    
    @abstractmethod
    async def save(self, recommendation: Recommendation) -> str:
        """
        Save the recommendation to the database.

        Args:
            recommendation (Recommendation): The recommendation to be saved.

        Returns:
            str: The ID of the saved recommendation.
        """
        pass

    @abstractmethod
    async def find_by_invoicer_id(self, invoice_id: str) -> Recommendation:
        """
        Retrieve a recommendation by the associated invoice ID.

        Args:
            invoice_id (str): The invoice ID associated with the recommendation.
        
        Returns:
            Recommendation: The recommendation corresponding to the provided invoice ID.
        """
        pass
