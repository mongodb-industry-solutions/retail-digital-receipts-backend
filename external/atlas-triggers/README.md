# ⚡ Atlas Trigger – Propagate Recommendations

This MongoDB Atlas Trigger listens to new inserts in the `recommendations` collection.

Its job is to copy recommendation results to two target collections:

- `users.lastRecommendations` → for frontend home rendering
- `invoices.recommendations` → for PDF rendering and invoice enrichment

---

## When is this Trigger invoked?

Every time `recommendation-ms` inserts a new document into the `recommendations` collection,  
this trigger runs automatically. It reads the full payload (`fullDocument`) and writes the data to other collections.

---

## Trigger Setup

| Setting        | Value                            |
|----------------|----------------------------------|
| Trigger Type   | Database Trigger                 |
| Operation Type | Insert                           |
| Database       | `your-database-name`             |
| Collection     | `recommendations`                |
| Full Document  | Enabled                          |
| Function Name  | `propagateRecommendations`       |

---

