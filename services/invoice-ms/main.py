import asyncio
import logging
from fastapi import FastAPI, Request, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.infrastructure.queue.async_queue import EventQueue
from app.infrastructure.events.change_listener import MongoChangeStream
from app.application.workers.event_processor import EventProcessor
from app.infrastructure.db.mongo_invoice_repository import MongoInvoiceRepository
from app.infrastructure.external_services.azure_metadata_enricher import AzureMetadataEnricher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# Set up CORS middleware
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

# Instantiate the concrete repository for invoices.
invoice_repository = MongoInvoiceRepository()

# Instantiate the external metadata service.
# Load the Azure metadata endpoint from an environment variable.
# Even if the URL is constant in production, using an environment variable
azure_endpoint = os.getenv("AZURE_METADATA_ENDPOINT", "https://your-azure-function-endpoint-url")
metadata_service = AzureMetadataEnricher(azure_endpoint)

# Instantiate the Worker (EventProcessor) by injecting the event queue, repository, and external metadata service.
worker = EventProcessor(event_queue, invoice_repository, metadata_service)

@app.on_event("startup")
async def on_startup():
    """
    On application startup, launch two background tasks:
    1) The Change Stream listener that detects MongoDB 'insert' events.
    2) The Worker (EventProcessor) that consumes events from the queue and processes them,
       including enriching invoices with external metadata.
    
    Both tasks run concurrently via asyncio, so the API remains responsive.
    """
    logger.info("Starting background tasks: Change Stream listener and EventProcessor.")
    # Task #1: Listen for MongoDB insert events.
    asyncio.create_task(change_stream.listen_for_changes())
    # Task #2: Continuously process events from the event queue.
    asyncio.create_task(worker.process_events())
    logger.info("Background tasks started successfully.")

# Include the router if you have additional endpoints.
app.include_router(router)
