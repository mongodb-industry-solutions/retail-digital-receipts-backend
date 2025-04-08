from app.domain.models.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepository
import logging

# Configure logging for tracking events and errors
logger = logging.getLogger(__name__)

class CreateInvoice:
    """
    The CreateInvoice class handles the business logic for creating an invoice from order data.
    
    It is a part of the use case layer, which orchestrates business processes. In this case, the process
    includes converting an order event into an invoice, performing necessary validations, and saving the 
    invoice into the database.

    This class delegates the task of saving the invoice to a repository (InvoiceRepository), which ensures 
    persistence. This separation allows for better testability and adheres to Clean Architecture principles.
    """

    def __init__(self, invoice_repository: InvoiceRepository):
        """
        Initialize the CreateInvoice use case.

        Args:
            invoice_repository (InvoiceRepository): The repository responsible for saving the invoice to the database.
        """
        self.invoice_repository = invoice_repository

    async def execute(self, order_data: dict):
        """
        Creates an invoice based on the order data and persists it to the database.

        Args:
            order_data (dict): The order data coming from the event (Change Stream).
        
        Returns:
            str: The ID of the created invoice.
        """
        try:
            # Step 1: Create an Invoice entity using the order data
            invoice = Invoice.from_order(order_data)

            # Step 2: Save the created invoice using the repository
            invoice_id = await self.invoice_repository.save(invoice)

            logger.info(f"Invoice successfully created for order ID {order_data['_id']} with invoice ID {invoice_id}")

            return invoice_id  # Return the ID of the created invoice

        except Exception as e:
            # Log any errors that occur during the invoice creation process
            logger.error(f"Error creating invoice for order ID {order_data['_id']}: {e}")
            raise  # Reraise the exception to be handled by the caller
