# ADR 001: Decision to Use Clean Architecture
 
**Date:** April 2025

## Context

We are developing the **Invoice and Recommendation Microservices** as part of a larger system. Although this is a **demo**, we want to follow industry standards and best practices to ensure that the code remains scalable, maintainable, and easy to extend. The goal is to create a robust, modular, and clear system that can easily be adapted or expanded with new features or integrations in the future.

The system needs to handle event-driven (like **MongoDB Change Streams**), band also needs to be flexible enough to support other use cases or integrate new tools over time. Therefore, it is essential to apply **Clean Architecture**, a widely adopted approach to software design that emphasizes separation of concerns, scalability, and maintainability.

## Decision

We decided to use **Clean Architecture** for this microservice for the following reasons:

1. **Separation of Concerns**:
   - **Clean Architecture** ensures a clear distinction between the **core business logic** (inside the **`domain/`** layer) and **infrastructure concerns** (inside the **`infrastructure/`** layer). By keeping these responsibilities separate, we make the system easier to maintain, test, and extend.

2. **Maintainability**:
   - The system is designed to be **modular** and **decoupled**, allowing changes to be made in one part of the system without affecting others. This makes it easy to modify, extend, or replace components like the **repository** or **event listener** without impacting core business logic.

3. **Scalability**:
   - The application follows a scalable architecture, allowing for future enhancements like switching event processing systems (e.g., replacing **MongoDB Change Streams** with **Kafka** or **Azure Event Bus**) without requiring a complete rewrite.

4. **Testability**:
   - By adhering to Clean Architecture, we ensure that business logic is isolated from infrastructure concerns, making it easier to test components independently. This allows for comprehensive **unit tests** for business logic and **integration tests** for infrastructure interactions.

5. **Flexibility for Future Changes**:
   - As new requirements arise, Clean Architecture allows the system to evolve. Whether we need to introduce new functionalities (e.g., supporting multiple event sources, integrating with a new payment system) or change infrastructure components, the architecture allows for these changes without disrupting the entire system.

6. **Public Code Standard**:
   - Since this project will be public, following a **standardized** and **well-known architecture** (like **Clean Architecture**) ensures that the code is understandable, maintainable, and usable by other developers. A clean, standardized structure helps others contribute to the project or use it as a reference in their own work.

### The File Structure

The project is organized following **Clean Architecture** principles, with clear separation between different layers:

 
### Explanation of Key Folders:
- **`domain/`**: Contains **core business models** like **Invoice** and **interfaces** for repositories. This layer is independent of any infrastructure.
- **`application/`**: Contains **use cases** like **`CreateInvoice`**, which implement business workflows.
- **`infrastructure/`**: Contains **implementations of external systems** (e.g., **MongoDB** repository, **Change Stream listener**).
- **`interfaces/`**: Contains the **API layer** (e.g., FastAPI routes) and data validation schemas.

### Consequences

### Advantages:
- **Modular and Decoupled**: The system is built with a **modular structure**, where each component is independent, making it easy to update or replace individual parts (like switching the event processing system).
- **Clear Separation**: **Clean Architecture** makes it easy to distinguish between different layers and responsibilities, improving code readability and maintainability.
- **Future-Proof**: The system is **designed to evolve**, with minimal impact on existing functionality when new features or technologies are introduced.
- **Easier to Test**: With clear separation between business logic and infrastructure, the system is easier to unit-test and integrate-test.

### Disadvantages:
- **Complexity for Small Projects**: The initial design might seem complex for a small demo or project, but it lays a solid foundation for future growth.
- **Learning Curve**: Developers who are not familiar with **Clean Architecture** may need some time to understand the structure and conventions.



