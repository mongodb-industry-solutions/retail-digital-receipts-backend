import asyncio
import logging
from app.infrastructure.queue.async_queue import EventQueue
from app.application.use_cases.create_invoice import CreateInvoice 

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventProcessor:
    """
    The EventProcessor class is a worker that processes events from the event queue. 
    It listens for events triggered by the MongoDB Change Stream and processes them to create invoices. 

    This class decouples the event listening mechanism from the business logic, ensuring that events are processed asynchronously 
    and efficiently without blocking the main application.

    The worker is responsible for consuming events from the queue, processing them, 
    and invoking the business logic (CreateInvoice) to generate the corresponding invoices.
    """

    def __init__(self, event_queue: EventQueue, create_invoice: CreateInvoice):
        """
        Initialize the EventProcessor.

        Args:
            event_queue (EventQueue): The queue where events are stored for processing.
            create_invoice (CreateInvoice): The use case responsible for creating invoices from events.
        """
        self.event_queue = event_queue
        self.create_invoice = create_invoice

    async def process_events(self):
        """
        Continuously process events from the event queue.

        This method listens for events in an asynchronous loop. It processes each event by passing it to the `CreateInvoice` use case, 
        which handles the business logic of creating an invoice. After processing each event, the task is marked as done.
        """
        while True:
            event = await self.event_queue.get()  # Wait for the next event in the queue
            if event:
                logger.info(f"Processing event: {event}")  # Log the event being processed
                try:
                    # Pass the event data (order) to the CreateInvoice use case
                    await self.create_invoice.execute(event["fullDocument"])  # Process the order data to create an invoice
                    logger.info(f"Successfully created invoice for order ID: {event['fullDocument']['_id']}")
                except Exception as e:
                    logger.error(f"Error while processing event for order ID {event['fullDocument']['_id']}: {e}")
                
            self.event_queue.task_done()  # Mark the event as processed once done
