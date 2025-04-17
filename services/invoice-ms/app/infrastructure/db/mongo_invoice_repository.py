from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.models.invoice import Invoice
from app.infrastructure.db.mongo_client import get_db
from bson import ObjectId

class MongoInvoiceRepository(InvoiceRepository):
    def __init__(self):
        """
        Initialize the repository with the MongoDB client and the 'invoices' collection.
        The `get_db()` function should return a singleton database instance.
        """
        self.db = get_db()
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

    def get_by_id(self, invoice_id: str) -> dict:
        """
        Retrieve a raw invoice document by its MongoDB ObjectId.
        
        Args:
            invoice_id (str): The ObjectId of the invoice as a string.
        
        Returns:
            dict: The invoice document, or None if not found.
        """
        return self.collection.find_one({"_id": ObjectId(invoice_id)})

    def update_rendered_file_url(self, invoice_id: str, file_url: str) -> None:
        """
        Update the invoice document with the rendered file URL.
        This is used to avoid regenerating the file if it already exists.
        
        Args:
            invoice_id (str): The ObjectId of the invoice as a string.
            file_url (str): The Blob Storage URL of the rendered file.
        """
        self.collection.update_one(
            {"_id": ObjectId(invoice_id)},
            {"$set": {"rendered_file_url": file_url}}
        )
