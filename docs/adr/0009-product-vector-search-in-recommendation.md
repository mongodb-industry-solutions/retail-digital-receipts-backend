
# ADR 0009 – Why Product Vector Search Lives in recommendation-ms (for now)

**Date:** April 2025

---

## What we know for sure

We're going to use vector search on the `products` collection — that’s not going to change any time soon.

Right now, `recommendation-ms` needs to access that data to generate suggestions.  
There’s no `product-ms` exposing embeddings as an API yet.

So doing the vector search **directly from here** is practical, legit, and unproblematic.

---

## But also...

If one day we do introduce a `product-ms`, it would make sense to move this search there — to respect clear data ownership boundaries.

Still, recommendation logic will likely grow in this service anyway, with:
- More complex business rules
- Custom ML models
- User-aware and context-based ranking

So it’s natural for `recommendation-ms` to evolve as the **brain of product suggestions**.

---

## Design-wise, this makes sense

Yes, this microservice reads from the product catalog.  
But the decision about *what to recommend and why* clearly belongs here.

As we said:

> “This could be migrated later — but the value lives here.”

That’s exactly why we’re using a **Port**:  
If tomorrow the way we fetch similar products changes (say, via HTTP to `product-ms`), the business logic stays intact.  
Only the adapter changes.

---

## A quick note on Ports & Adapters

- A **Port** defines *what the application needs* — in this case:  
  _“Give me a list of products similar to this embedding.”_  
  It’s a clean interface, with no technical details.

- An **Adapter** is *how we fulfill that request* — for now, it runs a MongoDB `$vectorSearch` query.  
  Later, it might call an external API instead.

> Using ports allows us to swap implementations without touching the core logic.

---

##  To revisit when `product-ms` becomes part of the system
