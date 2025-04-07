import os
import asyncio
import logging
from app.infrastructure.db.mongo_client import get_db  # Import the MongoDB client singleton
from app.infrastructure.queue.async_queue import EventQueue  # Import the event queue
from bson import ObjectId

# Configure logging to capture important events and errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MongoChangeStream:
    def __init__(self):
        """
        Initialize the MongoDB Change Stream watcher.
        
        The MongoDB client and database are obtained through the singleton `get_db()` function.
        This ensures that only one MongoDB client instance is created throughout the application's lifecycle.
        """
        self.db = get_db()  # Fetch the MongoDB database instance using the singleton client
        self.collection = self.db['orders']  # The collection to watch for changes (orders)
        self.event_queue = EventQueue()  # The event queue to pass changes to the worker for processing

    async def listen_for_changes(self):
        """
        Listens to changes in the 'orders' collection and pushes the changes to the event queue.
        
        The Change Stream will monitor insert operations and only process 'insert' type events.
        This ensures that only newly inserted orders are captured.
        """
        resume_token = None  # The token to resume from where it left off
        while True:
            try:
                # Watch for 'insert' operations only
                async for change in self.collection.watch(
                        [{"$match": {"operationType": "insert"}}],  # Filter for insert operations only
                        resume_after=resume_token):
                    logger.info(f"Change detected: {change}")  # Log the detected change
                    await self.event_queue.put(change)  # Push the change to the event queue
                    resume_token = change["_id"]  # Save the resume_token for the next iteration
            except Exception as e:
                logger.error(f"Error listening to changes: {e}")
                await asyncio.sleep(5)  # Retry after a short delay if an error occurs
