import httpx
import logging
from typing import Dict
from bson import ObjectId
from app.domain.services.external_metadata_service import ExternalMetadataService

logger = logging.getLogger(__name__)

def clean_object_ids(obj):
    """
    Recursively converts all ObjectId instances in a nested dictionary or list to strings.
    This is necessary because ObjectId is not JSON serializable, and Azure Functions
    expect standard JSON types.
    """
    if isinstance(obj, dict):
        return {k: clean_object_ids(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_object_ids(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    else:
        return obj

class AzureMetadataEnricher(ExternalMetadataService):
    """
    Concrete implementation of ExternalMetadataService that sends order data
    to an Azure Function to retrieve enriched invoice metadata.
    """

    def __init__(self, endpoint_url: str):
        """
        Initializes the service with the Azure Function endpoint URL.
        
        """
        self.endpoint_url = endpoint_url

    async def fetch_metadata(self, order_data: dict) -> Dict:
        """
        Sends the full order data to the Azure Function and receives enrichment metadata.

        - Cleans ObjectId fields so the payload is valid JSON.
        - Performs an asynchronous HTTP POST request to the Azure Function.
        - Logs any errors and returns an empty dictionary on failure.

        Args:
            order_data (dict): The order data dictionary received from MongoDB.

        Returns:
            Dict: The enrichment metadata from the Azure Function, or an empty dict if the request fails.
        """
        order_id = order_data.get("_id", "unknown")

        try:
            # Convert ObjectId fields to strings to make the payload JSON serializable
            cleaned_payload = clean_object_ids(order_data)

            async with httpx.AsyncClient() as client:
                response = await client.post(self.endpoint_url, json=cleaned_payload)
                response.raise_for_status()
                metadata = response.json()
                logger.info(f"Successfully fetched metadata from Azure Function for order {order_id}.")
                return metadata
        except Exception as e:
            logger.error(f"Error fetching metadata for order {order_id}: {e}")
            return {}
