"""
azure_blob_service.py – Upload helper for Azure Blob Storage

• Uses DefaultAzureCredential → Managed Identity in Azure, az login in local
• No connection string or account key required
"""

import os
from typing import BinaryIO

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient


class AzureBlobUploader:
    """Upload a stream to Azure Blob Storage and return its URL."""

    def __init__(self) -> None:
        self._account_url = os.getenv("AZURE_BLOB_ACCOUNT_URL")
        self._container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

        if not self._account_url or not self._container_name:
            raise ValueError("Missing AZURE_BLOB_ACCOUNT_URL or AZURE_BLOB_CONTAINER_NAME")

        self._credential = DefaultAzureCredential()

    # ------------------------------------------------------------------
    # public
    # ------------------------------------------------------------------
    def upload_file(self, file_name: str, file_stream: BinaryIO) -> str:
        """Upload the given stream as <file_name> and return the blob URL."""
        blob_client = BlobClient(
            account_url=self._account_url,
            container_name=self._container_name,
            blob_name=file_name,              # <- correct keyword
            credential=self._credential,
        )
        blob_client.upload_blob(file_stream, overwrite=True)
        return blob_client.url