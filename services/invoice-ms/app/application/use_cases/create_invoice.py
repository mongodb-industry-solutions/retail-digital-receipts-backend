from app.domain.models.invoice import Invoice
from app.domain.repositories.invoice_repository import InvoiceRepository
from app.domain.services.external_metadata_service import ExternalMetadataService
import logging
import asyncio

logger = logging.getLogger(__name__)

class CreateInvoice:
    """
    The CreateInvoice class handles the business logic for creating an invoice from order data.
    It enriches the invoice with metadata from an external service before saving.
    """

    def __init__(self, 
                 invoice_repository: InvoiceRepository, 
                 external_metadata_service: ExternalMetadataService,
                 max_retries: int = 3):
        """
        Initialize the CreateInvoice use case.

        Args:
            invoice_repository (InvoiceRepository): The repository for saving invoices.
            external_metadata_service (ExternalMetadataService): The service for fetching enrichment metadata.
            max_retries (int): Number of retry attempts for metadata enrichment.
        """
        self.invoice_repository = invoice_repository
        self.external_metadata_service = external_metadata_service
        self.max_retries = max_retries

    async def execute(self, order_data: dict) -> str:
        """
        Creates and saves an invoice from the order data after enriching it with external metadata.

        Args:
            order_data (dict): The order data used to create the invoice.

        Returns:
            str: The ID of the created invoice.
        """
        invoice = Invoice.from_order(order_data)

        # Step 1: Try to enrich the invoice with external metadata
        for attempt in range(1, self.max_retries + 1):
            try:
                metadata = await asyncio.wait_for(
                    self.external_metadata_service.fetch_metadata(order_data),
                    timeout=5  # Optional timeout per attempt
                )
                invoice.enrich(metadata)
                logger.info(f"Successfully enriched invoice for order ID {order_data['_id']}")
                break
            except Exception as e:
                logger.warning(f"[Attempt {attempt}] Metadata enrichment failed: {e}")
                if attempt == self.max_retries:
                    logger.error("Max retries reached. Proceeding without enrichment.")

        # Step 2: Save the invoice
        try:
            invoice_id = await self.invoice_repository.save(invoice)
            logger.info(f"Invoice created for order ID {order_data['_id']} with ID {invoice_id}")
            return invoice_id
        except Exception as e:
            logger.error(f"Failed to save invoice for order ID {order_data.get('_id')}: {e}")
            raise
