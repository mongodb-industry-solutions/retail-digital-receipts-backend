# app/domain/models/recommendation_group.py
from dataclasses import dataclass
from datetime import datetime
from typing import List
from .recommendation_item import RecommendationItem

@dataclass
class RecommendationGroup:
    user_id: str
    invoice_id: str
    created_at: datetime
    items: List[RecommendationItem]
