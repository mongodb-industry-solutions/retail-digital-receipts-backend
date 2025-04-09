from app.domain.models.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.services.external_metadata_service import ExternalMetadataService
import logging

logger = logging.getLogger(__name__)

class CreateInvoice:
    """
    The CreateInvoice class handles the business logic for creating an invoice from order data.
    It now also calls an external metadata service to enrich the invoice before saving.
    """

    def __init__(self, 
                 invoice_repository: InvoiceRepository, 
                 external_metadata_service: ExternalMetadataService):
        """
        Initialize the CreateInvoice use case.

        Args:
            invoice_repository (InvoiceRepository): The repository for saving invoices.
            external_metadata_service (ExternalMetadataService): The service responsible for fetching external metadata.
        """
        self.invoice_repository = invoice_repository
        self.external_metadata_service = external_metadata_service

    async def execute(self, order_data: dict) -> str:
        """
        Creates and saves an invoice from the order data after enriching it with external metadata.

        Args:
            order_data (dict): The data from which to create the invoice.
        
        Returns:
            str: The ID of the created invoice.
        """
        try:
            # Step 1: Create an Invoice entity
            invoice = Invoice.from_order(order_data)
            
            # Step 2: Enrich the invoice using the external metadata service
            metadata = await self.external_metadata_service.fetch_metadata(str(order_data["_id"]))
            invoice.enrich(metadata)
            
            # Step 3: Persist the enriched invoice using the repository
            invoice_id = await self.invoice_repository.save(invoice)
            
            if invoice_id:
                logger.info(f"Invoice successfully created for order ID {order_data['_id']} with invoice ID {invoice_id}")
            else:
                logger.error(f"Failed to create invoice for order ID {order_data['_id']}")
            
            return invoice_id
        except Exception as e:
            logger.error(f"Error creating invoice for order ID {order_data.get('_id')}: {e}")
            raise
