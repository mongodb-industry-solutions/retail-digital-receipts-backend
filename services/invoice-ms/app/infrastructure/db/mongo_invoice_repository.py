from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.models.invoice import Invoice
from app.infrastructure.db.mongo_client import get_db

class MongoInvoiceRepository(InvoiceRepository):
    def __init__(self):
        """
        Initialize the repository with the MongoDB client and the 'invoices' collection.
        The `get_db()` function should return a singleton client or database instance.
        """
        self.db = get_db()         # Shared (singleton) database reference
        self.collection = self.db["invoices"]

    async def save(self, invoice: Invoice) -> str:
        """
        Save the generated invoice to the 'invoices' collection.
        
        Args:
            invoice (Invoice): The invoice entity to be saved.
        
        Returns:
            str: The inserted invoice ID.
        """
        invoice_dict = invoice.to_dict()
        result = await self.collection.insert_one(invoice_dict)
        return str(result.inserted_id)

    async def find_by_order_id(self, order_id: str) -> Invoice | None:
        """
        Retrieve an invoice by its associated order ID.
        
        Args:
            order_id (str): The order ID associated with the invoice.
        
        Returns:
            Invoice | None: The found invoice or None if not found.
        """
        invoice_doc = await self.collection.find_one({"orderId": order_id})
        if invoice_doc:
            return Invoice.from_order(invoice_doc)
        return None
