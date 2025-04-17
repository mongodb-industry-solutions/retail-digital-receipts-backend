from azure.storage.blob import BlobServiceClient
from typing import BinaryIO
import os
from dotenv import load_dotenv

load_dotenv()

class AzureBlobUploader:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        container_name = os.getenv("AZURE_BLOB_CONTAINER_NAME")
        if not connection_string or not container_name:
            raise ValueError("Missing connection string or container name")

        self.client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = container_name

    def upload_file(self, file_name: str, file_stream: BinaryIO) -> str:
        blob_client = self.client.get_blob_client(container=self.container_name, blob=file_name)
        blob_client.upload_blob(file_stream, overwrite=True)
        return blob_client.url
