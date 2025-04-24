"""
Main entrypoint – Recommendation Microservice

Software Design Notes (for students/devs):

This microservice follows an Event-Driven Architecture using Clean Architecture principles.

- The system listens to new invoices (via MongoDB Change Streams).
- Events are placed in an in-memory queue.
- A background worker (EventProcessor) consumes the events and runs the business logic.
- All dependencies are injected (DI) for testability and separation of concerns.
- MongoDB Atlas Vector Search is used to retrieve similar products.
- Recommendations are written to the database and propagated via Atlas Triggers.

This design avoids tight coupling and keeps responsibilities clear:
-Mongo handles data & events
-The microservice applies business rules
-Triggers handle side effects (like updating the user and invoice documents)

Great for learning:
-Clean code structure
-Real-world tech like Change Streams & Vector Search
-Easy to scale, test, and evolve
"""


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
from app.infrastructure.vector_search.mongodb_vector_search_adapter import MongoDBVectorSearchAdapter

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

    # Initialize the recommendation repository
    recommendation_repository = MongoRecommendationRepository()

    # Initialize the Vector Search adapter
    vector_search_port = MongoDBVectorSearchAdapter()

    # Initialize the event processor (worker)
    worker = EventProcessor(
        event_queue=event_queue,
        recommendation_repository=recommendation_repository,
        vector_search_port=vector_search_port
    )

    logger.info("Launching background tasks: MongoDB listener and EventProcessor.")

    # Run both listener and processor concurrently
    await asyncio.gather(
        change_stream.listen_for_changes(),
        worker.process_events()
    )

if __name__ == "__main__":
    # Entry point of the microservice
    asyncio.run(main())
