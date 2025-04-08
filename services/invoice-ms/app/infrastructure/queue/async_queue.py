import asyncio
import logging

logger = logging.getLogger(__name__)

class EventQueue:
    """
    The EventQueue class is a wrapper around asyncio.Queue and is used to store and manage events asynchronously.
    
    It is designed to act as an event queue that allows different components of the system (like the Change Stream
    listener and worker) to communicate by passing events. The queue allows events to be processed one by one in an
    asynchronous manner, ensuring that each event is handled without blocking other processes.
    
    This class is ideal for decoupling the event production (Change Stream) from event consumption (Worker), enabling
    scalable and efficient event-driven processing in a non-blocking, asynchronous environment.
    """

    def __init__(self):
        """
        Initialize the event queue using asyncio.Queue.
        This queue will hold the events that need to be processed asynchronously.
        """
        self.queue = asyncio.Queue()

    async def put(self, item):
        """
        Put an item (event) into the queue.
        
        Args:
            item (dict): The event to put in the queue.
        """
        # Extract info for logging
        operation_type = item.get("operationType", "unknown")
        doc_id = item.get("documentKey", {}).get("_id", "no_id")

        logger.info(
            "Enqueuing event (operationType=%s) for doc_id=%s.",
            operation_type,
            doc_id
        )

        await self.queue.put(item)

    async def get(self):
        """
        Get an item (event) from the queue.
        
        Returns:
            dict: The event that is fetched from the queue.
        """
        item = await self.queue.get()
        # Extract info for logging
        operation_type = item.get("operationType", "unknown")
        doc_id = item.get("documentKey", {}).get("_id", "no_id")

        logger.info(
            "Dequeued event (operationType=%s) for doc_id=%s.",
            operation_type,
            doc_id
        )

        return item

    def task_done(self):
        """
        Mark the task as done after processing the event.
        
        This method should be called by the worker to indicate that the event has been processed.
        """
        self.queue.task_done()
