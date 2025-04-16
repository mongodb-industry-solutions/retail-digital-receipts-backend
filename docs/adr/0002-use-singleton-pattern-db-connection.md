# ADR: Singleton Pattern for AsyncIOMotorClient in FastAPI with MongoDB

**Date:** April 2025

## Context

Our FastAPI application interacts with MongoDB for two primary purposes:

1. **Data Persistence:** Storing invoice data reliably.
2. **Real-Time Event Listening:** Utilizing MongoDB Change Streams to monitor the 'orders' collection for insert events.

## Why Use the Singleton Pattern with Async MongoDB and Change Streams?

### Efficient Resource Management

Creating a single instance of `AsyncIOMotorClient` ensures that your application maintains only one connection pool to MongoDB. This reduces the overhead associated with establishing multiple connections and helps prevent exceeding the database's connection limits.

### Stable Change Stream Operations

MongoDB Change Streams rely on a persistent connection to monitor real-time data changes. By using a singleton client, you ensure that the Change Stream listener maintains a continuous and reliable connection, which is essential for accurate event detection.

### Consistent Database Access

Having a single, shared database client instance across your application components promotes consistency and simplifies the management of database operations. This is especially important in asynchronous environments where multiple coroutines might interact with the database concurrently.

## Implementation Highlights

### Singleton Client Initialization

Your `get_db()` function checks if the `_client` and `_db` variables are `None` before creating a new `AsyncIOMotorClient` instance. This lazy initialization ensures that the client is created only once and reused thereafter.

### Shared Access Across Components

By importing the `db` instance from your database module, different parts of your application, such as repositories and event listeners, can access the same database connection without creating new clients.

### Integration with Change Streams

Your `MongoChangeStream` component utilizes the shared `db` instance to watch for changes in the 'orders' collection. This setup allows your application to respond to new orders in real-time, triggering the invoice creation process seamlessly.

## Conclusion

Implementing the Singleton pattern for your asynchronous MongoDB client in FastAPI is a sound architectural decision, especially when working with features like Change Streams that require persistent connections. This approach enhances the efficiency, stability, and maintainability of your application.

For a deeper understanding of the Singleton pattern, refer to [Refactoring Guru's Singleton Pattern](https://refactoring.guru/design-patterns/singleton).

