# ADR-0005: Repository Pattern for Invoice Persistence
 
**Date:** April 2025

## Context
The persistence of invoice data should be decoupled from business logic to allow flexibility and avoid tight coupling to the infrastructure. The Repository pattern is an appropriate way to implement this persistence, as it abstracts database operations and allows the infrastructure to be changed without affecting the business logic. This pattern is documented for the current invoice microservice but is intended to be reusable for other microservices.

## Decision
We have implemented the Repository pattern with the `InvoiceRepository` class, which defines persistence methods for invoices, such as `save` and `find_by_order_id`. The concrete class `MongoInvoiceRepository` implements this interface and handles the interaction with MongoDB.

## Implementation

- `InvoiceRepository` defines the operations that should be performed on invoices, regardless of the database used. This provides a flexible foundation for interacting with different data sources if required in future microservices.

- `MongoInvoiceRepository` is the concrete implementation that interacts with MongoDB using the Singleton pattern to avoid unnecessary multiple connections.

This separation allows changing the database or infrastructure without affecting the business logic, and it provides a reusable structure for other microservices that require similar data persistence patterns.
