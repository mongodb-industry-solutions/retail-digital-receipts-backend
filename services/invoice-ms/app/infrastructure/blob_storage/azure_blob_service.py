"""
azure_blob_service.py
─────────────────────
Blob‑storage helper that uploads files and verifies blob existence
using Azure Managed Identity (DefaultAzureCredential).

No connection string or account key required.
"""

from __future__ import annotations

import os
from typing import BinaryIO

from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient


class AzureBlobUploader:
    """
    Thin wrapper around azure‑storage‑blob that supports two operations:

    • upload_file(file_name, stream) → str   (returns blob URL)
    • blob_exists(file_name)        → bool

    The storage account and container are provided via environment vars:

        AZURE_BLOB_ACCOUNT_URL   e.g. https://myacct.blob.core.windows.net/
        AZURE_BLOB_CONTAINER_NAME
    """

    def __init__(self) -> None:
        account_url = os.getenv("AZURE_BLOB_ACCOUNT_URL")
        container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

        if not account_url or not container_name:
            raise ValueError(
                "Both AZURE_BLOB_ACCOUNT_URL and AZURE_BLOB_CONTAINER_NAME "
                "must be set in the environment."
            )

        self._account_url: str = account_url
        self._container_name: str = container_name
        self._credential = DefaultAzureCredential()

    # --------------------------------------------------------------------- #
    # Public API                                                             #
    # --------------------------------------------------------------------- #
    def upload_file(self, file_name: str, file_stream: BinaryIO) -> str:
        """
        Upload *file_stream* as *file_name* and return the blob URL.
        Overwrites any existing blob with the same name.
        """
        blob_client = self._client(file_name)
        blob_client.upload_blob(file_stream, overwrite=True)
        return blob_client.url

    def blob_exists(self, file_name: str) -> bool:
        """True if the blob is present in the target container."""
        try:
            self._client(file_name).get_blob_properties()
            return True
        except ResourceNotFoundError:
            return False

    # --------------------------------------------------------------------- #
    # Internal helper                                                        #
    # --------------------------------------------------------------------- #
    def _client(self, blob_name: str) -> BlobClient:
        """Create a BlobClient for the given blob name."""
        return BlobClient(
            account_url=self._account_url,
            container_name=self._container_name,
            blob_name=blob_name,
            credential=self._credential,
        )
