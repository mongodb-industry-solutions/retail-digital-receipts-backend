from fastapi import APIRouter, HTTPException
from app.infrastructure.db.mongo_invoice_repository import MongoInvoiceRepository
from app.shared.utils.pdf_renderer import InvoiceRenderer
from app.infrastructure.blob_storage.azure_blob_service import AzureBlobUploader
from app.application.use_cases.render_invoice import RenderInvoiceIfNotExistsUseCase
from app.interfaces.schemas.invoice_response import InvoiceFileResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/invoices/{invoice_id}/file", response_model=InvoiceFileResponse)
async def get_invoice_file(invoice_id: str):
    """
    Single endpoint to obtain (or generate) the rendered invoice file in Blob Storage.

    Behavior:
    - If the invoice exists and has already been rendered → returns the stored download URL.
    - If the invoice exists but has not been rendered → renders, uploads to Azure Blob, saves the URL, and returns it.
    - If the invoice does not exist → returns 404 Not Found.

    Notes:
    - This endpoint is idempotent and safe to call multiple times.
    - It does NOT create invoices from scratch. They must already exist in MongoDB.
    """
    try:
        # Get the invoice from MongoDB (singleton connection)
        repo = MongoInvoiceRepository()
        invoice = await repo.get_by_id(invoice_id)

        if not invoice:
            raise HTTPException(status_code=404, detail="Invoice not found")

        # Return existing rendered file URL if already available
        if invoice.get("rendered_file_url"):
            logger.info(f"Invoice {invoice_id} already rendered. Returning cached URL.")
            return {
                "invoice_id": invoice_id,
                "download_url": invoice["rendered_file_url"]
            }

        # Render and upload the file on demand
        logger.info(f"Invoice {invoice_id} not rendered yet. Generating now...")
        renderer = InvoiceRenderer()
        uploader = AzureBlobUploader()
        use_case = RenderInvoiceIfNotExistsUseCase(repo, renderer, uploader)

        result = await use_case.execute(invoice_id)
        logger.info(f"Invoice {invoice_id} rendered and uploaded successfully.")

        return result

    except HTTPException:
        raise  # Re-raise expected HTTP errors

    except Exception as e:
        logger.exception(f"Unexpected error while generating invoice file: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating invoice file."
        )
