# app/infrastructure/vector_search/vector_search_mapper.py

"""
Infrastructure Mapper – Vector Search Results

Maps raw MongoDB Atlas Vector Search documents into domain-level \`RecommendationItem\` objects.
Keeps the domain model isolated from database-specific fields and formats.
"""

from app.domain.models.recommendation_item import RecommendationItem

def map_vector_search_result(doc: dict) -> RecommendationItem:
    """
    Convert a raw Vector Search hit into a domain RecommendationItem.

    Args:
        doc (dict): A single document from the $vectorSearch aggregation pipeline.

    Returns:
        RecommendationItem: The corresponding domain object.
    """
    return RecommendationItem(
        product_id=doc["productId"],
        name=doc.get("name", ""),
        brand=doc.get("brand", ""),
        price=doc.get("price", 0.0),
        image=doc.get("image", ""),
        vector_search_score=doc.get("vectorSearchScore", 0.0),
    )