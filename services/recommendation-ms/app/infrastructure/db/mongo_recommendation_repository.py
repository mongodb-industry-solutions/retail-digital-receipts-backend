# app/infrastructure/db/mongo_recommendation_repository.py

"""
Infrastructure adapter: MongoDB repository for RecommendationGroup documents.

Responsible ONLY for persistence details; business logic lives in the application layer.
"""

import logging
from typing import Optional
from bson import ObjectId
from datetime import datetime
from motor.motor_asyncio import AsyncIOMotorCollection

from app.domain.repositories.recommendation_repository import RecommendationRepository
from app.domain.models.recommendation_group import RecommendationGroup
from app.domain.models.recommendation_item import RecommendationItem
from app.infrastructure.db.mongo_client import get_db  # singleton helper

logger = logging.getLogger(__name__)

class MongoRecommendationRepository(RecommendationRepository):
    """
    Concrete implementation of the RecommendationRepository port
    using Motor (async MongoDB driver).
    """

    def __init__(self) -> None:
        db = get_db()  # singleton Motor database
        self.collection: AsyncIOMotorCollection = db["recommendations"]
        logger.info("MongoRecommendationRepository initialised (collection: recommendations)")

    async def save(self, group: RecommendationGroup) -> str:
        """
        Persist a new RecommendationGroup and return its inserted ID.
        """
        doc = {
            "userId": group.user_id,
            "invoiceId": group.invoice_id,
            "createdAt": group.created_at or datetime.utcnow(),
            "items": [
                {
                    "productId": item.product_id,
                    "name": item.name,
                    "brand": item.brand,
                    "price": item.price,
                    "image": item.image,
                    "vectorSearchScore": item.vector_search_score
                }
                for item in group.items
            ],
        }
        result = await self.collection.insert_one(doc)
        logger.debug(
            "Saved recommendations for invoice %s (id=%s)",
            group.invoice_id, result.inserted_id
        )
        return str(result.inserted_id)

    async def find_by_invoice_id(self, invoice_id: str) -> Optional[RecommendationGroup]:
        """
        Fetch recommendations by invoiceId.
        """
        doc = await self.collection.find_one({"invoiceId": invoice_id})
        if not doc:
            logger.debug("No recommendations found for invoice %s", invoice_id)
            return None

        items = [
            RecommendationItem(
                product_id = item["productId"],
                name = item["name"],
                brand = item["brand"],
                price = item["price"],
                image = item["image"],
                vector_search_score = item["vectorSearchScore"]
            )
            for item in doc.get("items", [])
        ]

        group = RecommendationGroup(
            user_id = doc["userId"],
            invoice_id = doc["invoiceId"],
            created_at = doc.get("createdAt", datetime.utcnow()),
            items = items
        )
        logger.debug("Loaded recommendations for invoice %s", invoice_id)
        return group

    async def get_by_id(self, rec_id: str) -> Optional[dict]:
        """
        Retrieve the raw MongoDB document by its ObjectId.
        """
        doc = await self.collection.find_one({"_id": ObjectId(rec_id)})
        if doc:
            logger.debug("Found recommendation document id=%s", rec_id)
        else:
            logger.debug("Recommendation id=%s not found", rec_id)
        return doc
