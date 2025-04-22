from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.storage.blob import (
    BlobServiceClient,
    generate_blob_sas,
    BlobSasPermissions,
)


def build_sas_url(
    account_url: str,
    container: str,
    blob_name: str,
    ttl_minutes: int = 15,
) -> str:
    """
    Create a read‑only SAS URL valid for `ttl_minutes`.
    Works with Managed Identity by using a User Delegation Key.
    """

    # Use the managed identity token
    credential = DefaultAzureCredential()
    service = BlobServiceClient(account_url=account_url, credential=credential)

    # Start / expiry for the SAS
    start = datetime.utcnow()
    expiry = start + timedelta(minutes=ttl_minutes)

    # Get a user‑delegation key signed by Azure AD
    delegation_key = service.get_user_delegation_key(
        key_start_time=start,
        key_expiry_time=expiry,
    )

    # Build the SAS token
    account_name = account_url.split("//")[1].split(".")[0]
    sas_token = generate_blob_sas(
        account_name=account_name,
        container_name=container,
        blob_name=blob_name,
        permission=BlobSasPermissions(read=True),
        expiry=expiry,
        user_delegation_key=delegation_key,
    )

    return f"{account_url}{container}/{blob_name}?{sas_token}"
