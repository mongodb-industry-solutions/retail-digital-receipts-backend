# ADR: Use of MongoDB Lookup for Embedding Retrieval in Recommendation Microservice

**Date:** April 2025

## Context
In the current setup of our demo, the `recommendation-ms` needs to access product embeddings to perform vector searches. These embeddings are critical for identifying products similar to those in a customer's recent order. The main challenge is that embeddings are stored in the `products` collection, and the recommendation microservice doesn't directly interact with this collection under normal operations.

## Decision
Implement a MongoDB lookup operation within the `recommendation-ms` to retrieve embeddings directly from the `products` collection at runtime. This approach temporarily bypasses the need for a dedicated product microservice or extended inter-service communication, simplifying the demo architecture.

## Rationale
- **Simplicity:** Maintains a simple demo setup without multiplying microservices.
- **Performance:** Localizes data retrieval to MongoDB, utilizing its efficient lookup capabilities.
- **Scalability:** Easily refactorable once a more complex service architecture (including a dedicated products microservice) is warranted.

## Implications
- **Technical Debt:** Introduces some technical debt as it embeds product-specific logic within the `recommendation-ms`, which we need to address in future iterations.
- **Coupling:** Increases coupling between `recommendation-ms` and the product data schema, making future schema changes potentially disruptive.

## Future Considerations
- **Decoupling Services:** As the demo evolves or moves towards a production environment, consider deploying a dedicated products microservice that manages embeddings and handles vector search requests.
- **Cache Implementations:** If performance becomes an issue due to frequent MongoDB lookups, implementing a caching layer could mitigate overhead.
