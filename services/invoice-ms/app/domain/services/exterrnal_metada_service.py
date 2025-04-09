from abc import ABC, abstractmethod
from typing import Dict

class ExternalMetadataService(ABC):
    """
    Abstract interface for fetching external metadata for an order.
    This defines the contract that any external metadata service must follow.
    """

    @abstractmethod
    async def fetch_metadata(self, order_id: str) -> Dict:
        """
        Fetch external metadata for a given order.

        Args:
            order_id (str): The ID of the order for which metadata is requested.

        Returns:
            Dict: A dictionary containing the metadata.
        """
        pass
