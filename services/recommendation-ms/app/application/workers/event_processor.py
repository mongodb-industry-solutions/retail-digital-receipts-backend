import asyncio
import logging
from app.infrastructure.queue.async_queue import EventQueue
from app.application.use_cases.generate_recommendation import GenerateRecommendation
from app.domain.ports.vector_search_port import VectorSearchPort
from app.domain.repositories.recommendation_repository import RecommendationRepository

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventProcessor:
    """
    The EventProcessor class is a worker that processes events from the event queue.
    It consumes invoice creation events and triggers the business logic to generate recommendations.
    """

    def __init__(
        self,
        event_queue: EventQueue,
        recommendation_repository: RecommendationRepository,
        vector_search_port: VectorSearchPort
    ):
        """
        Initialize the EventProcessor.

        Args:
            event_queue (EventQueue): The queue where invoice events are stored for processing.
            recommendation_repository (RecommendationRepository): The repository used to persist recommendations.
            vector_search_port (VectorSearchPort): The port used to perform vector similarity search.
        """
        self.event_queue = event_queue
        self.generate_recommendation_use_case = GenerateRecommendation(vector_search_port, recommendation_repository)

    async def process_events(self):
        """
        Continuously process invoice events from the event queue.
        """
        while True:
            event = await self.event_queue.get()  # Wait for the next invoice event
            if event:
                try:
                    logger.info(f"Processing invoice event: {event}")

                    invoice_data = event.get("fullDocument")
                    if not invoice_data or "_id" not in invoice_data:
                        logger.error("Malformed invoice event data: %s", event)
                    else:
                        invoice_id = invoice_data["_id"]
                        logger.info(f"Generating recommendation for invoice ID: {invoice_id}")
                        
                        success = await self.generate_recommendation_use_case.execute(invoice_data)
                        if success:
                            logger.info(f"✅ Recommendation generated and saved for invoice ID: {invoice_id}")
                        else:
                            logger.warning(f"⚠️ Recommendation skipped for invoice ID: {invoice_id}")
                except Exception as e:
                    logger.error("Error while processing invoice event: %s", e)

            self.event_queue.task_done()  # Mark the event as processed
