 ADR 0009 – Why Recommendation-MS Performs Vector Search Directly on the ODL Product Catalog

**Date:** April 2025 *(Updated December 2025)*  
**Status:** Accepted

## Context

In classic microservice architecture guidance, the rule of thumb is:

> Each service owns its data.  
> Other services must consume that data through APIs, not by querying its database.

Initially, we assumed this rule applied strictly here — that `recommendation-ms` should access product data only through a future `product-ms`.

However, after revisiting our assumptions, analyzing trade-offs using *Software Architecture: The Hard Parts*, and considering both modern MongoDB capabilities and the Operational Data Layer (ODL) pattern, we realized that this assumption does not fully apply in our design.

Our system does not have private, per-service databases. Instead:

> Upstream systems feed MongoDB Atlas, which acts as an **Operational Data Layer** — a governed, shared **Product Data Domain** used by multiple consumers.

`recommendation-ms` is **not** reading someone else’s private store.  
It is consuming a **shared, contract-driven domain model**.

## Forces and Trade-offs

| Force | Preference | Consequence |
|-------|-----------|-------------|
| Service autonomy | Separate data ownership | Hard to unify data across services |
| Real-time personalization | Single low-latency view | API chaining becomes expensive |
| Microservice decoupling | API contracts | Heavy orchestration for AI/search |
| Modern MongoDB capabilities | Single operational platform | Classic guidance needs rethinking |

Classic approaches assumed no database could support diverse workloads.  
MongoDB now provides:

- Flexible document model
- Vector, full-text, and hybrid search
- Workload isolation
- Change Streams and event-driven sync

Those capabilities enable a shared, governed ODL without reintroducing a shared DB anti-pattern.

## ODL vs. Shared Database

A shared database is:

❌ multiple services writing to the same tables  
❌ schema coupling  
❌ accidental dependencies

An **Operational Data Layer** is:

✔️ a **read-optimized**, governed Product Data Domain  
✔️ fed by upstream systems (ERP, Order Service, etc.)  
✔️ exposes **contracted data views**, not internal schemas  
✔️ enables multiple consumers without API chaining

In the ODL:

- Producers own how data is written
- Consumers read from stable, versioned contracts

`recommendation-ms` consuming the `catalog` collection is **Data-as-a-Service**, not DB sharing.

## Why Vector Search Lives in Recommendation-MS

The Recommendation domain owns:

- Interpreting user actions
- Using embeddings for semantic similarity
- Applying ranking rules and business context
- Generating omnichannel suggestions

To do this, it needs:

1. **Direct access** to the shared Product Data Domain  
2. **Local control** of `$vectorSearch` execution  
3. A **stable contract** for product data, not API orchestration

Even if `product-ms` is introduced later, it would become **another producer or API**, not the owner of recommendation logic.

The **value** lives here:

> Deciding *what* to recommend and *why*, not just retrieving similar products.

## Ports & Adapters

To avoid coupling recommendation logic with data retrieval details, `recommendation-ms` uses a **Port**:

**Port:**  
```text
Given a product (or embedding), return similar catalog items.
```

**Current Adapter:**  
Executes MongoDB `$vectorSearch` on the ODL `catalog` collection.

**Future Adapter Options:**  
- `product-ms` HTTP endpoint  
- Dedicated retrieval service  
- Alternative embedding store

The domain logic remains unchanged.

## Decision

We **keep vector search in `recommendation-ms`**, running against the Product Data Domain in the ODL.

This is acceptable because:

- Reads are **read-only** and governed by contract schemas  
- The ODL is intentionally shared and versioned  
- MongoDB supports real-time, search-ready operational workloads  
- The Recommendation domain must own similarity and ranking logic

No refactor is required.



## Summary

❌ Anti-pattern  
Querying another service’s private operational database

✅ Valid pattern  
Consuming a **shared Product Data Domain** within an **Operational Data Layer**, designed for real-time search, personalization, and AI

`recommendation-ms` operates according to the latter.
