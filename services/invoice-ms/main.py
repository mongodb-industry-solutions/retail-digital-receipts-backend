import asyncio
import logging
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.infrastructure.queue.async_queue import EventQueue
from app.infrastructure.events.change_listener import MongoChangeStream
from app.application.workers.event_processor import EventProcessor
from app.infrastructure.db.mongo_invoice_repository import MongoInvoiceRepository


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

router = APIRouter()

@app.get("/")
async def read_root(request: Request):
    """
    A basic route to confirm the server is running.
    """
    return {"message": "Server is running"}

# Create a single, shared event queue for passing events between tasks.
# Note: The queue itself is NOT a separate background task; it's just an in-memory
# structure used by the two background tasks (the Change Stream listener and the Worker).
event_queue = EventQueue()

# Instantiate the Change Stream listener (producer),
# which watches the 'orders' collection for 'insert' events.
change_stream = MongoChangeStream(event_queue)

# Instantiate the concrete repository for invoices
invoice_repository = MongoInvoiceRepository()

# Instantiate the Worker (consumer) that processes events from the queue.
worker = EventProcessor(event_queue, invoice_repository)

@app.on_event("startup")
async def on_startup():
    """
    On application startup, launch two background tasks:
    1) The Change Stream listener that detects MongoDB 'insert' events.
    2) The Worker that consumes events from the queue and processes them.

    Both tasks run concurrently via asyncio, so the API remains responsive.
    """
    logger.info("Starting background tasks: Change Stream listener and Worker.")
    # Task #1: Listen for MongoDB inserts
    asyncio.create_task(change_stream.listen_for_changes())
    # Task #2: Continuously process events from the queue
    asyncio.create_task(worker.process_events())
    logger.info("Background tasks started successfully.")

# Include the router if you have additional endpoints
app.include_router(router)
