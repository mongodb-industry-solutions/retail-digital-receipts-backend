"""
invoice.py – HTTP routes for the Invoice microservice
─────────────────────────────────────────────────────
Exposes a single GET endpoint that delivers a time‑limited (15‑minute)
SAS URL for downloading an invoice PDF stored in Azure Blob Storage.

Behaviour
  • Valid ID & file already rendered   → returns fresh SAS URL
  • Valid ID & file not rendered       → renders PDF, uploads, persists URL,
      then returns SAS URL
  • Non‑existent invoice              → 404
  • Malformed ID (not a valid ObjectId)→ 400
  • Other errors                      → 500

The heavy work (render, upload, URL signing) is delegated to the
RenderInvoiceIfNotExistsUseCase.  Azure access uses Managed Identity;
no storage keys or public containers are required.
"""
import logging
from fastapi import APIRouter, HTTPException
from bson.errors import InvalidId

from app.infrastructure.db.mongo_invoice_repository import MongoInvoiceRepository
from app.shared.utils.pdf_renderer import InvoiceRenderer
from app.infrastructure.blob_storage.azure_blob_service import AzureBlobUploader
from app.application.use_cases.render_invoice import RenderInvoiceIfNotExistsUseCase
from app.interfaces.schemas.invoice_response import InvoiceFileResponse

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/invoices/{invoice_id}/file", response_model=InvoiceFileResponse)
async def get_invoice_file(invoice_id: str):
    try:
        repo = MongoInvoiceRepository()
        renderer = InvoiceRenderer()
        uploader = AzureBlobUploader()
        use_case = RenderInvoiceIfNotExistsUseCase(repo, renderer, uploader)

        result = await use_case.execute(invoice_id)
        logger.info(
            "Invoice %s ready – SAS URL issued (expires %s min).",
            invoice_id,
            result["expires_in"],
        )
        return result

    except InvalidId as err:
        # Malformed ObjectId
        raise HTTPException(status_code=400, detail="Invalid invoice_id") from err

    except ValueError as err:
        # Document not found
        raise HTTPException(status_code=404, detail=str(err)) from err

    except Exception as err:
        logger.exception("Unexpected error while generating invoice file: %s", err)
        raise HTTPException(
            status_code=500,
            detail="Internal server error while generating invoice file.",
        ) from err
