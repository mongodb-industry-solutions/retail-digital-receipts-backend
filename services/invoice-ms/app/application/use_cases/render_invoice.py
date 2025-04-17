from app.domain.repositories.invoice_repository import InvoiceRepository
from app.shared.utils.pdf_renderer import InvoiceRenderer
from app.infrastructure.blob_storage.azure_blob_service import AzureBlobUploader


class RenderInvoiceIfNotExistsUseCase:
    def __init__(
        self,
        invoice_repo: InvoiceRepository,
        renderer: InvoiceRenderer,
        uploader: AzureBlobUploader
    ):
        """
        Use case to render an invoice file (PDF) if it doesn't already exist.

        Args:
            invoice_repo (InvoiceRepository): Repository to access and update invoices.
            renderer (InvoiceRenderer): Responsible for generating PDF from invoice data.
            uploader (AzureBlobUploader): Responsible for uploading the rendered file to Blob Storage.
        """
        self.invoice_repo = invoice_repo
        self.renderer = renderer
        self.uploader = uploader

    async def execute(self, invoice_id: str) -> dict:
        """
        Main use case logic.

        Args:
            invoice_id (str): The MongoDB ObjectId of the invoice.

        Returns:
            dict: Contains invoice_id and download_url.
        """
        # Step 1: Retrieve the invoice document from MongoDB
        invoice = await self.invoice_repo.get_by_id(invoice_id)
        if not invoice:
            raise ValueError(f"Invoice not found with ID: {invoice_id}")

        # Step 2: If the invoice already has a file URL, return it directly
        if invoice.get("rendered_file_url"):
            return {
                "invoice_id": invoice_id,
                "download_url": invoice["rendered_file_url"]
            }

        # Step 3: Generate the PDF file using the renderer (returns file path)
        file_path = self.renderer.render(invoice)

        # Step 4: Open and upload the file to Blob Storage
        file_name = f"invoice_{invoice_id}.pdf"
        with open(file_path, "rb") as file_stream:
            file_url = self.uploader.upload_file(file_name, file_stream)

        # Step 5: Update the invoice document with the file URL
        self.invoice_repo.update_rendered_file_url(invoice_id, file_url)


        # Step 6: Return the download URL
        return {
            "invoice_id": invoice_id,
            "download_url": file_url
        }
