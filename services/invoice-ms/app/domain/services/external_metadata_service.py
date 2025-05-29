from abc import ABC, abstractmethod
from typing import Dict

class ExternalMetadataService(ABC):
    """
    Abstract interface for fetching external metadata for an order.
    This defines the contract that any external metadata service must follow.
    """

    @abstractmethod
    async def fetch_metadata(self, order_data: dict) -> Dict:
        """
        Fetch external metadata for a given order.

        Args:
            order_data (dict): The complete order data to be enriched with external metadata.

        Returns:
            Dict: A dictionary containing the enrichment metadata.
        """
        pass
