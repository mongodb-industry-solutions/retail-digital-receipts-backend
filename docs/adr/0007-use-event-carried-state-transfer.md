# ADR 0007 – Event-Carried State Transfer for Recommendation Data

**Date:** April 2025

## 1 Context  
`recommendation-ms` produces four product suggestions for every new invoice.  
The frontend already reads:

- `users.lastRecommendations`
- `invoices.recommendations`

It should keep working with a single read per view.

---

## 2 Easy but rejected option  
Let **`recommendation-ms` write directly into `users` and `invoices`**.

Drawbacks  
- Tight coupling to schemas it does not own.  
- Any change in user or invoice collections forces code changes in `recommendation-ms`.  
- Blurs service boundaries: one MS updates another MS’s data.

---

## 3 Decision – use Event-Carried State Transfer (ECST)

1. `recommendation-ms` stores the full recommendation document in its own
   `recommendations` collection.
2. MongoDB emits an `insert` event containing that entire document (`fullDocument`).
3. A lightweight Atlas Trigger consumes the event and copies the payload to  
   - `users.lastRecommendations`  
   - `invoices.recommendations`

`recommendation-ms` writes only to data it owns; duplication happens outside the service.

---

## 4 Why ECST is better

| Aspect            | Direct write (rejected) | ECST (chosen)            |
|-------------------|-------------------------|--------------------------|
| Coupling          | Service tied to foreign schemas | Services remain independent |
| Schema evolution  | Change breaks the MS    | Only the trigger adapts  |
| Domain clarity    | Responsibilities mixed  | Clear ownership          |
| UI read pattern   | One read                | One read (unchanged)     |

---

## 5 Consequences

- Each microservice touches only its own data.  
- Frontend stays fast (still one document read).  
- Future schema changes in user or invoice documents require changes only in the trigger, not in `recommendation-ms`.

**Status: Accepted**
