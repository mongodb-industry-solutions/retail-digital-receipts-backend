# ADR-0004: Asynchronous Event Processing with asyncio Queue

**Date:** April 2025

## Context
The application needs to process events asynchronously to avoid blocking the main execution thread, particularly when dealing with events coming from MongoDB Change Streams. In order to maintain the application's responsiveness, a system is required to receive and process these events efficiently.

We aim to decouple the event production (Change Stream listener) from the event consumption (EventProcessor) to facilitate scalable event-driven processing in a non-blocking, asynchronous environment.

Additionally, while the current solution uses an in-memory queue, this could potentially be replaced by a more scalable event-processing system like an event bus or Kafka in the future.

## Decision
We have chosen to implement an asynchronous event queue using `asyncio.Queue` to handle events efficiently. The events from MongoDB Change Streams are placed into the queue, and a dedicated worker asynchronously processes these events. 

This solution ensures that events are processed in a non-blocking manner, allowing the system to handle multiple events concurrently without affecting overall performance. Furthermore, we’ve made the system modular, which allows for future integration with other event-processing tools or systems if necessary.

## Implementation

The solution consists of the following key components:

1. **EventQueue**: 
    - A wrapper around `asyncio.Queue` that stores and manages events asynchronously.
    - This class decouples the event production (Change Stream listener) from event consumption (EventProcessor), ensuring efficient communication between components. 
    - Events are put into the queue by the `MongoChangeStream` listener and consumed by the `EventProcessor` worker.

2. **MongoChangeStream**:
    - Listens to the `orders` collection in MongoDB and detects insert events.
    - Events from these MongoDB operations are placed into the `EventQueue`.

3. **EventProcessor**:
    - An asynchronous worker that processes events from the `EventQueue`.
    - The worker executes the necessary logic, such as invoice creation and interaction with external services like Azure, for enriching invoices with metadata.
    - By using the asynchronous approach, multiple events can be processed concurrently without blocking the main thread.

4. **Scalability Considerations**:
    - The system is designed to be scalable and flexible. While `asyncio.Queue` is used as an in-memory queue for simplicity, this can be replaced in the future with a more robust event-processing system like an event bus or Kafka. This would provide enhanced scalability and resilience for handling high throughput in a distributed environment.

5. **Start-up Task Management**:
    - At application startup, two background tasks are initiated:
        1. The `MongoChangeStream` listener, which detects "insert" operations on the MongoDB `orders` collection.
        2. The `EventProcessor` worker, which processes the queued events and handles the invoice creation and enrichment.
    - These tasks run concurrently via `asyncio`, ensuring that the API remains responsive and capable of handling multiple events efficiently.
