# ADR 0010 – Handling External Enrichment in `invoice-ms`

## Context

In this demo, `invoice-ms` enriches each invoice by calling an external Azure Function.  
We’ve added basic resilience: the call has retries and timeout, and if it fails, we still save the invoice without metadata.

This makes sense for a prototype — we want to see the full flow working and keep things simple.

---

## But in a real production system…

Calling an external service (especially one critical to invoice data) during creation is risky.

If the service is:
- Slow
- Temporarily down
- Unavailable for hours or days

…it will **delay or block invoice creation**, even if everything else works fine.

---

## What we would do in production

We’d handle enrichment **asynchronously**, using domain events:

1. `invoice-ms` saves the invoice immediately  
2. It emits an `InvoiceCreated` event  
3. Another service picks it up and performs enrichment later  
4. When ready, it updates the invoice or emits `InvoiceEnriched`

This avoids coupling invoice creation to external systems.

---

## Summary

- We implemented retries and fallback for now — good enough for the demo  
- In production, enrichment should be handled separately and asynchronously  
- Invoices should never depend on the real-time availability of external systems
