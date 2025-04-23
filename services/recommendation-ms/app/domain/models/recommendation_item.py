# app/domain/models/recommendation_item.py
from dataclasses import dataclass

@dataclass
class RecommendationItem:
    """
    Domain model representing a recommended product, to be embedded
    in the user's profile and optionally associated with the invoice.

    This object is typically generated via Vector Search based on
    product similarity.
    """
    product_id: str
    name: str
    brand: str
    price: float
    image: str
    vector_search_score: float
