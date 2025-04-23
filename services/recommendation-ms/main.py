import asyncio
import logging
import os
from dotenv import load_dotenv

# Queue and background processing
from app.infrastructure.queue.async_queue import EventQueue
from app.infrastructure.events.change_listener import MongoChangeStream
from app.application.workers.event_processor import EventProcessor

# Repositories and services
from app.infrastructure.db.mongo_recommendation_repository import MongoRecommendationRepository
from app.infrastructure.vector_search.mongo_vector_search_adapter import MongoVectorSearchAdapter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env.local
load_dotenv()

async def main():
    logger.info("Starting Recommendation Microservice...")

    # Create a shared async queue to exchange events between listener and worker
    event_queue = EventQueue()

    # Initialize the MongoDB Change Stream listener (event producer)
    change_stream = MongoChangeStream(event_queue)

    # Initialize the recommendation repository for writing recommendation results
    recommendation_repository = MongoRecommendationRepository()

    # Initialize the Vector Search adapter to perform similarity queries
    vector_search_service = MongoVectorSearchAdapter()

    # Initialize the event processor (worker) with the necessary dependencies
    worker = EventProcessor(
        event_queue=event_queue,
        recommendation_repository=recommendation_repository,
        vector_search_service=vector_search_service
    )

    logger.info("Launching background tasks: MongoDB listener and EventProcessor.")

    # Run the listener and worker concurrently using asyncio
    await asyncio.gather(
        change_stream.listen_for_changes(),
        worker.process_events()
    )

if __name__ == "__main__":
    # Entry point of the microservice
    asyncio.run(main())
