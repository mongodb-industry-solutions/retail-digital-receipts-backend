import os
import asyncio
import logging
from app.infrastructure.db.mongo_client import get_db
from app.infrastructure.queue.async_queue import EventQueue
from bson import ObjectId

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoChangeStream:
    """
    Monitors the 'orders' collection in MongoDB, but only listens for 'insert' events.
    When an insert occurs, the event is enqueued for asynchronous processing.

    In this demo’s business logic, each new order triggers the generation of an invoice.
    By filtering only 'insert' events, we ensure that the workflow starts only when a new
    order document is created, which occurs when a checkout is processed.
    """

    def __init__(self, event_queue):
        """
        Initializes the MongoChangeStream with a reference to an existing event queue  
        - Retrieves a singleton MongoDB client (via get_db()).
        - Selects the 'orders' collection to watch.
        """
        self.db = get_db()
        self.collection = self.db["orders"]
        self.event_queue = event_queue   # <-- Use the queue you passed in

    async def listen_for_changes(self):
        """
        Continuously listens for 'insert' changes on the 'orders' collection.

        - Uses MongoDB's Change Stream with a filter pipeline to detect only inserts.
        - When an insert is detected, logs the event and enqueues it for further processing.
        - Utilizes a resume token so the listener can recover from interruptions.
        - Retries automatically on errors, waiting 5 seconds before resuming.
        """
        resume_token = None

        while True:
            try:
                # Only match 'insert' events
                pipeline = [{"$match": {"operationType": "insert"}}]

                # If a resume token exists, resume from there
                options = {"resume_after": resume_token} if resume_token else {}

                async for change in self.collection.watch(pipeline, **options):
                    operation_type = change.get("operationType", "unknown")
                    doc_id = change.get("documentKey", {}).get("_id")

                    logger.info(
                        "Detected '%s' operation on document ID '%s'. Enqueuing the event...",
                        operation_type,
                        doc_id
                    )

                    # Enqueue the insert event
                    await self.event_queue.put(change)
                    logger.info("Successfully enqueued event for doc ID '%s'.", doc_id)

                    # Update the resume token to resume here on restart
                    resume_token = change["_id"]
                    logger.info("Updated resume token")

            except Exception as e:
                logger.error(
                    "Error while listening for insert changes in 'orders' collection: %s. "
                    "Retrying in 5 seconds.",
                    e
                )
                await asyncio.sleep(5)
