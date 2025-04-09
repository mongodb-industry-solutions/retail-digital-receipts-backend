import httpx
import logging
from typing import Dict
from app.domain.services.external_metadata_service import ExternalMetadataService

logger = logging.getLogger(__name__)

class AzureMetadataService(ExternalMetadataService):
    """
    Concrete implementation of ExternalMetadataService that fetches metadata from an Azure Function.
    """

    def __init__(self, endpoint_url: str):
        """
        Initialize the service with the Azure Function endpoint URL.

        Args:
            endpoint_url (str): The URL of the Azure Function providing metadata.
        """
        self.endpoint_url = endpoint_url

    async def fetch_metadata(self, order_id: str) -> Dict:
        """
        Fetch external metadata for the given order ID from the Azure Function.

        Args:
            order_id (str): The order ID to fetch metadata for.

        Returns:
            Dict: A dictionary with the metadata returned by the Azure Function, or an empty dict on error.
        """
        try:
            async with httpx.AsyncClient() as client:
                # Prepare the payload. Adjust as needed for your Azure Function.
                payload = {"order_id": order_id}
                response = await client.post(self.endpoint_url, json=payload)
                response.raise_for_status()
                metadata = response.json()
                logger.info("Successfully fetched metadata from Azure Function.")
                return metadata
        except Exception as e:
            logger.error(f"Error fetching metadata for order {order_id}: {e}")
            return {}
