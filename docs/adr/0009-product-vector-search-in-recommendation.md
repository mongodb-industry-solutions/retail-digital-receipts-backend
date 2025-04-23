# ADR 0009 – Product Vector Search Lives in recommendation-ms (for now)

**Date:** April 2025

## 1. Context

We don’t yet have a dedicated `product-ms`.  
But `recommendation-ms` needs to find similar products based on what a user just bought, to generate recommendations.

Since product embeddings already live in the shared `products` collection, we’re doing the vector search here — inside `recommendation-ms`.

---

## 2. Decision

We perform the product vector search directly in `recommendation-ms`, using MongoDB Atlas Vector Search.

Even though this touches product data, the goal is **recommending items**, so the logic fits well here — at least for now.

We wrap the search behind a `VectorSearchPort`, so we can easily move it later if needed.

---

## 3. Why this is okay for now
- `product-ms` doesn’t exist yet
- This avoids premature complexity
- The logic here is **read-only**
- And the port-based design keeps us flexible

---

## 4.📌 We’ll revisit this when `product-ms` becomes part of the architecture