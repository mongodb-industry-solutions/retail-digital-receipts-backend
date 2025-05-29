# app/interfaces/schemas/invoice_response.py
from pydantic import BaseModel

class InvoiceFileResponse(BaseModel):
    invoice_id: str
    download_url: str
    expires_in: int   # minutes the SAS URL is valid