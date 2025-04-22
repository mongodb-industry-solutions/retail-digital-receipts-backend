# infrastructure/blob_storage/azure_blob_service.py
from azure.storage.blob import BlobClient
from azure.identity import DefaultAzureCredential
from typing import BinaryIO
import os

class AzureBlobUploader:
    def __init__(self):
        account_url = os.getenv("AZURE_BLOB_ACCOUNT_URL")
        container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")

        if not account_url or not container_name:
            raise ValueError("Missing account URL or container name")

        #  DefaultAzureCredential, use Managed Identity in Azure
        self._credential = DefaultAzureCredential()
        self._account_url = account_url
        self._container_name = container_name

    def upload_file(self, file_name: str, file_stream: BinaryIO) -> str:
        blob_client = BlobClient(
            account_url=self._account_url,
            container_name=self._container_name,
            blob=file_name,
            credential=self._credential,
        )
        blob_client.upload_blob(file_stream, overwrite=True)
        return blob_client.url

