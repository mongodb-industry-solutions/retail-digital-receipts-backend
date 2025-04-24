from datetime import datetime
from typing import List, Dict, Optional
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class Invoice:
    """
    Domain entity representing an invoice.
    Designed to be framework-agnostic and independent of infrastructure.
    """

    def __init__(
        self,
        order_id: str,
        user_id: str,
        items: List[Dict],
        created_at: Optional[datetime] = None,
        metadata: Optional[Dict] = None,
        recommendations: Optional[List[Dict]] = None,
        status: str = "created",
        _id: Optional[ObjectId] = None
    ):
        self._id = _id
        self.order_id = order_id
        self.user_id = user_id
        self.items = items
        self.created_at = created_at or datetime.utcnow()
        self.metadata = metadata or {}
        self.recommendations = recommendations or []
        self.status = status
        self.validate()

    def validate(self):
        if not self.order_id or not self.user_id:
            raise ValueError("Order ID and User ID are required")

    def calculate_total(self) -> float:
        return sum(item['price']['amount'] for item in self.items)

    def enrich(self, external_data: Dict):
        self.metadata.update(external_data)

    def to_dict(self) -> Dict:
        invoice_dict = {
            "orderId": self.order_id,
            "userId": self.user_id,
            "items": self.items,
            "createdAt": self.created_at.isoformat(),
            "metadata": self.metadata,
            "recommendations": self.recommendations,
            "status": self.status,
            "totalAmount": self.calculate_total()
        }

        if self._id:
            invoice_dict["_id"] = self._id
            invoice_dict["invoiceId"] = str(self._id)

        return invoice_dict

    @staticmethod
    def from_order(order: Dict, _id: Optional[ObjectId] = None):
        invoice = Invoice(
            order_id=order["_id"],
            user_id=order["user"],
            items=order["products"],
            _id=_id
        )
        logger.info(f"Generated invoice: {invoice.to_dict()}")
        return invoice
