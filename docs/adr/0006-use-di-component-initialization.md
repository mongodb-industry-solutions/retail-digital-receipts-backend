# ADR-0006: Dependency Injection and Component Initialization

**Date:** April 2025

## Context

To ensure modularity and scalability, we need a way to manage dependencies between components, keeping services loosely coupled. Dependency Injection (DI) helps achieve this by centralizing component initialization and making components interchangeable and easier to test.

## Decision

We implemented **Dependency Injection (DI)** to manage and inject components (e.g., queues, repositories, services) into workers. This approach decouples component initialization from usage, promoting flexibility and reusability.

### Key Points:
- **EventQueue** manages event handling asynchronously.
- **MongoInvoiceRepository** abstracts MongoDB database interactions.
- **AzureMetadataEnricher** fetches external metadata for enriching invoices.
- These components are injected into the **EventProcessor** worker, which processes the events.
  
This DI pattern ensures that new microservices can reuse the same structure by swapping or adding different components as needed.

## Implementation

1. **EventQueue**: Shared queue for event-driven processing, reusable in any MS requiring async event handling.
2. **MongoInvoiceRepository**: Repository for MongoDB interactions, easily replaceable for other database types in future MSs.
3. **AzureMetadataEnricher**: External service for metadata enrichment, can be replaced with any other service in different MSs.
4. **EventProcessor**: Worker that processes events, using the injected components.

### Reusability:
The same DI pattern applies to other MSs by injecting components into a worker, promoting consistency across services and easing maintenance and testing.

## Consequences

- **Flexibility**: Easily replace or extend components (e.g., database or external services).
- **Testability**: Simplified unit testing by mocking dependencies.
- **Scalability**: Seamless addition of new services following the same architecture.

This DI approach ensures scalable, maintainable, and testable microservices.
