from app.domain.models.invoice import Invoice
from abc import ABC, abstractmethod

class InvoiceRepository(ABC):
    """
    The InvoiceRepository interface defines the methods needed to interact with the persistence layer for invoices.
    
    The purpose of this interface is to decouple the business logic from the specific infrastructure being used 
    (e.g., MongoDB). This allows for flexibility in changing the database or storage solution without affecting the core application.
    
    Methods:
        save(invoice: Invoice) -> str: Saves an invoice to the database.
        find_by_order_id(order_id: str) -> Invoice: Retrieves an invoice by its associated order ID.
    """
    
    @abstractmethod
    async def save(self, invoice: Invoice) -> str:
        """
        Save the invoice to the database.

        Args:
            invoice (Invoice): The invoice to be saved.

        Returns:
            str: The ID of the saved invoice.
        """
        pass

    @abstractmethod
    async def find_by_order_id(self, order_id: str) -> Invoice:
        """
        Retrieve an invoice by the associated order ID.

        Args:
            order_id (str): The order ID associated with the invoice.
        
        Returns:
            Invoice: The invoice corresponding to the provided order ID.
        """
        pass
