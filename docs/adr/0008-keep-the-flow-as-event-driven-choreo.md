# ADR 0006 – Keep the Flow as Event-Driven Choreography

**Date:** April 2025

## 1 Context  
Our retail-demo backend is a four-step pipeline:

1. **orders** collection receives a new order.  
2. **invoice-ms** listens to that insert and creates an invoice.  
3. **recommendation-ms** listens to the invoice insert and writes a recommendations document.  
4. An **Atlas Trigger** listens to the recommendations insert and projects the data into  
   `users.lastRecommendations` and `invoices.recommendations`.

No component calls another directly; each reacts to the event stream.

---

## 2 Problem  
A central “process manager” (orchestrator) could call each step in turn, but that would:

* become a single point of failure and a scaling bottleneck,  
* concentrate business logic in one service,  
* re-introduce synchronous dependencies we try to avoid.

---

## 3 Decision – Event-Driven Choreography  
We keep the pipeline as **pure choreography**:

* Every step owns exactly one action and one collection.  
* Ordering is implicit in the sequence of inserts (order → invoice → recommendations).  
* No service needs the URL or schema of its successor; it just watches the previous collection.

---

## 4 Why this is better

| Concern              | Orchestrator (rejected) | Choreography (chosen) |
|----------------------|-------------------------|-----------------------|
| Failure isolation    | A bug halts the chain   | A bug pauses one step |
| Scaling              | Central node can choke  | Each step scales alone|
| Ownership of logic   | All in one place        | Logic lives with its data |
| Adding a new step    | Modify orchestrator     | Just listen to events |

---

## 5 Consequences  

* **Loose coupling** – services depend only on MongoDB’s change stream, not on each other’s APIs.  
* **Elastic scaling** – each microservice can be scaled or rewritten independently.  
* **Clear responsibility** – a team owns one step and one collection.  
* **Easy extension** – future services can join the dance by listening to the right insert.

