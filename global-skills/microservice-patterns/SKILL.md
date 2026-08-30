---
name: microservice-patterns
description: Principles, resilience patterns, and architectural guidelines for synchronous distributed microservices in Go, PHP, and Python. Use when designing inter-service communication, handling partial failures (timeouts, retries, circuit breakers), or maintaining data integrity across service boundaries.
---

# Synchronous Microservices Reference Guide

Guidelines for a distributed system of **synchronous** (REST/JSON, gRPC) service-to-service microservices **without Event-Driven Architecture**. Applies to Go, PHP (Symfony), and Python (FastAPI) services.

---

## 1. Inter-Service Communication & Boundaries

* **Service Autonomy**: Each service owns its database exclusively. Never allow direct database-to-database connections across service boundaries — all access goes through the owning service's API.
* **API Contracts**:
  * Design backward-compatible REST/JSON or gRPC interfaces: semantic versioning, additive-only schema changes (new fields with defaults, never remove/rename existing ones).
  * Enforce strict contract boundaries via **Anti-Corruption Layers (ACLs)** in consuming services (see `domain-driven-design` skill, §6.2).
* **Data Duplication vs. Distributed Joins**:
  * Avoid synchronous multi-hop queries (Service A → Service B → Service C) to build a single view.
  * Cache or replicate stable reference data locally rather than making real-time cross-service queries for static attributes.
  * Accept that a read model is eventually consistent; don't build request-time fan-out graphs.

---

## 2. Resilience Patterns (Handling Partial Failures)

In synchronous microservices, a failure in one downstream dependency must not crash the upstream system.

* **Timeouts**: Every HTTP/gRPC outbound call MUST have an explicit, short timeout (e.g., connect timeout: 500ms, read timeout: 2-3s). Defaults that "never time out" are a bug.
* **Retries with Exponential Backoff & Jitter**: Only retry transient failures (HTTP 502/503/504, connection reset, timeouts) — never 4xx client errors. Add jitter to avoid thundering herds.
* **Circuit Breaker**: Trip the breaker when downstream failure rates exceed a threshold (e.g., 5 consecutive failures → open for 30s) to prevent cascading thread/socket exhaustion. Fail fast while open.
* **Bulkheads**: Isolate connection pools per downstream service so one failing service cannot consume all available workers.
* **Graceful Degradation / Fallbacks**: Return cached data, default values, or a degraded response when a non-critical downstream service fails. Only propagate hard failure for critical paths.

---

## 3. Distributed State & Data Integrity

* **Idempotency Keys**:
  * For non-idempotent operations (POST requests modifying state/payments), require a caller-supplied `Idempotency-Key` header so retries are safe.
  * Server stores the key + response; duplicate keys return the stored response instead of re-executing.
* **Two-Phase Dual Write Hazard**:
  * Writing to the local DB and immediately calling an external service in the same transaction is prone to partial failure (the outbound call cannot be rolled back).
  * *Rule:* Commit the local transaction first; if the outbound call fails, record a **pending sync state** to be retried by a background worker.
* **No Distributed Transactions**: Never use 2PC across service databases. Use synchronous orchestration + compensating actions (see `domain-driven-design` skill, §6.3).

---

## 4. Observability Across Boundaries

* **Correlation / Trace IDs**:
  * Generate a unique `X-Correlation-ID` (or OpenTelemetry `traceparent`) at the API gateway/edge.
  * Propagate the ID across all downstream HTTP/gRPC headers: Go (`context.Context`), Symfony (`RequestStack` / middleware), Python (`structlog` / `ContextVars`).
* **Structured Logging**: Log in JSON with consistent fields: `timestamp`, `level`, `correlation_id`, `service`, `message`, `error`. Never log secrets, tokens, or full request bodies with credentials.
* **Health Checks & Metrics**: Expose `/healthz` and `/readyz` (liveness vs. readiness) and per-downstream failure metrics so circuit breakers and degraded states are visible.