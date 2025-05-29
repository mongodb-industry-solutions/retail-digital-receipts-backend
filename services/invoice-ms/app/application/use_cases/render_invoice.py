from app.domain.repositories.invoice_repository import InvoiceRepository
from app.shared.utils.pdf_renderer import InvoiceRenderer
from app.infrastructure.blob_storage.azure_blob_service import AzureBlobUploader
from app.shared.utils.azure_sas import build_sas_url
from app.infrastructure.config.settings import settings


class RenderInvoiceIfNotExistsUseCase:
    """
    Render the invoice PDF (if needed), upload to Blob Storage,
    and return a short-lived SAS URL.
    """

    def __init__(
        self,
        invoice_repo: InvoiceRepository,
        renderer: InvoiceRenderer,
        uploader: AzureBlobUploader,
        sas_ttl_minutes: int = 15,
    ):
        self.invoice_repo = invoice_repo
        self.renderer = renderer
        self.uploader = uploader
        self.sas_ttl_minutes = sas_ttl_minutes

    async def execute(self, invoice_id: str) -> dict:
        """
        Returns:
            {
                "invoice_id": <str>,
                "download_url": <signed-url>,
                "expires_in": <minutes>
            }
        """
        # Retrieve invoice document
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice not found: {invoice_id}")

        file_name = f"invoice_{invoice_id}.pdf"

        # Re-render if no URL stored or blob was deleted
        if not invoice.get("rendered_file_url") or not self.uploader.blob_exists(file_name):
            # Render PDF locally
            file_path = self.renderer.render(invoice)

            # Upload to Azure Blob Storage
            with open(file_path, "rb") as file_stream:
                file_url = self.uploader.upload_file(file_name, file_stream)

            # Persist raw blob URL
            self.invoice_repo.update_rendered_file_url(invoice_id, file_url)

        # Always build a fresh SAS URL for the caller
        sas_url = build_sas_url(
            settings.azure_blob_account_url,
            settings.azure_blob_container_name,
            file_name,
            ttl_minutes=self.sas_ttl_minutes,
        )

        return {
            "invoice_id": invoice_id,
            "download_url": sas_url,
            "expires_in": self.sas_ttl_minutes,
        }
