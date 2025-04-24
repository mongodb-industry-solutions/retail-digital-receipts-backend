from app.domain.models.recommendation_item import RecommendationItem

def map_vs_result(doc: dict) -> RecommendationItem:
    """Convert a raw Vector Search hit into a domain RecommendationItem."""
    return RecommendationItem(
        product_id         = doc["productId"],
        name               = doc["name"],
        brand              = doc["brand"],
        price              = doc["price"],
        image              = doc["image"],
        vector_search_score= doc["vectorSearchScore"],
    )
