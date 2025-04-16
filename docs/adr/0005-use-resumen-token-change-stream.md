# ADR-0005: Handling MongoDB Change Stream Resume Token
 
**Date:** April 2025

---

## Context

We implemented the resume_token feature to ensure that the system can resume event processing from where it left off after a restart or temporary disconnection. After each event is processed, the resume_token is stored, and on reconnect, the Change Stream listener uses this token to continue processing from the last known event.

---

## Decision

- **Token Storage:** Save the resume token persistently after processing each event.
- **Stream Resumption:** On reconnection, resume processing from the last stored token.

---

## Consequences

- **Fault Tolerance:** Prevents loss of events during failures or restarts.
- **Reliability:** Ensures exactly-once event processing, increasing overall system resilience.

---
## References

- [MongoDB Change Streams - Resume a Change Stream](https://www.mongodb.com/docs/manual/changeStreams/#resume-a-change-stream)  