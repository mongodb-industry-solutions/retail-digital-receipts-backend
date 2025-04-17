from pydantic import BaseModel

class InvoiceFileResponse(BaseModel):
    invoice_id: str
    download_url: str
