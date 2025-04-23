from app.domain.repositories.recommendation_repository import RecommendationRepository
from app.domain.models.recommendation import Recommendation
from app.infrastructure.db.mongo_client import get_db
from bson import ObjectId

class MongoRecommendationRepository(RecommendationRepository):
    def __init__(self):
        """
        Initialize the repository with the MongoDB client and the 'recommendation' collection.
        The `get_db()` function should return a singleton database instance.
        """
        self.db = get_db()
        self.collection = self.db["recommendations"]

    async def save(self, recommendation: Recommendation) -> str:
        """
        Save the generated recommendation to the 'recommendations' collection.
        
        Args:
            recommendation (Recommendation): The recommedation entity to be saved.
        
        Returns:
            str: The inserted recommendation ID.
        """
        recommendation_dict = recommendation.to_dict()
        result = await self.collection.insert_one(recommendation_dict)
        return str(result.inserted_id)

    async def find_by_invoice_id(self, invoice_id: str) -> Recommendation| None:
        """
        Retrieve a recommendation by its associated invoice ID.
        
        Args:
            invoice_id (str): The invoice ID associated with the recommendation.
        
        Returns:
            Recommendation | None: The found recommendation or None if not found.
        """
        recommendation_doc = await self.collection.find_one({"invoiceId": invoice_id})
        if recommendation_doc:
            return Recommendation.from_invoice(recommendation_doc)
        return None

    def get_by_id(self, recommendation_id: str) -> dict:
        """
        Retrieve a raw recommendation document by its MongoDB ObjectId.
        
        Args:
            recommendation_id (str): The ObjectId of the recommendation as a string.
        
        Returns:
            dict: The recommendation document, or None if not found.
        """
        return self.collection.find_one({"_id": ObjectId(recommendation_id)})
