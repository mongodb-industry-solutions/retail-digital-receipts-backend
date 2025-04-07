from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.models.invoice import Invoice
from app.infrastructure.db.mongo_client import get_db

class MongoInvoiceRepository(InvoiceRepository):
    def __init__(self):
        """
        Initialize the repository with the MongoDB client and the invoices collection.
        The `get_db()` function ensures that the MongoDB client is a singleton.
        """
        self.db = get_db()  # Get the MongoDB database instance (Singleton)
        self.collection = self.db["invoices"]  # Mongo collection to store invoices

    async def save(self, invoice: Invoice) -> str:
        """
        Save the generated invoice to the MongoDB database.

        Args:
            invoice (Invoice): The invoice to be saved.

        Returns:
            str: The inserted invoice ID.
        """
        invoice_dict = invoice.to_dict()  # Convert the invoice entity to a dictionary
        result = await self.collection.insert_one(invoice_dict)  # Insert the invoice into MongoDB
        return str(result.inserted_id)  # Return the inserted ID

    async def find_by_order_id(self, order_id: str) -> Invoice:
        """
        Retrieve an invoice by its associated order ID.

        Args:
            order_id (str): The order ID associated with the invoice.
        
        Returns:
            Invoice: The invoice corresponding to the provided order ID.
        """
        invoice_doc = await self.collection.find_one({"orderId": order_id})  # Query MongoDB for the invoice
        if invoice_doc:
            return Invoice.from_order(invoice_doc)  # Convert the Mongo document to an Invoice entity
        return None  # Return None if no invoice is found
