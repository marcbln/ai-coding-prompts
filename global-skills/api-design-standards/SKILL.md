---
name: api-design-standards
description: Guidelines, contract standards, and best practices for designing robust, predictable, and maintainable REST/JSON and gRPC APIs across Go, PHP, and Python.
---

# API Design Standards Skill

Guidelines for building clean, consistent, and developer-friendly APIs in synchronous microservice ecosystems.

---

## 1. RESTful URL & Verb Conventions
- **Resource-Oriented URIs**: Use plural nouns for resource collections (`/orders`, `/users`, `/invoices`).
  - *Bad:* `/createOrder`, `/getUserById?id=1`, `/orders/update/123`
  - *Good:* `POST /orders`, `GET /users/1`, `PATCH /orders/123`
- **Sub-resources**: Express nested hierarchies cleanly (`/customers/42/orders`). Do not exceed 2 levels of nesting (prefer top-level resources with filter params: `GET /orders?customer_id=42`).
- **HTTP Method Semantics**:
  - `GET`: Safe, idempotent. Retrieve data only; no side effects.
  - `POST`: Non-idempotent. Create a new subordinate resource or execute a complex operation.
  - `PUT`: Idempotent. Complete replacement of the resource representation.
  - `PATCH`: Idempotent / Non-idempotent. Partial update using a JSON merge patch.
  - `DELETE`: Idempotent. Remove a resource.

---

## 2. Standard HTTP Status Codes

| Code | Usage | Guideline |
|---|---|---|
| **200 OK** | Successful read or synchronous update/action. | Always return the updated/requested payload. |
| **201 Created** | Successful creation via `POST`. | Include `Location` header pointing to the new resource. |
| **204 No Content** | Successful deletion or action with no body. | Do not return any response body. |
| **400 Bad Request** | Malformed syntax, unparseable JSON/headers. | Reserve for structural parsing failures. |
| **401 Unauthorized** | Missing or invalid authentication credentials. | User identity is unverified. |
| **403 Forbidden** | Authenticated, but lacking permission (RBAC/ownership). | Do not leak existence if forbidden. |
| **404 Not Found** | Resource or endpoint does not exist. | |
| **409 Conflict** | State conflict (e.g., duplicate unique constraint, state machine transition failure). | |
| **422 Unprocessable Entity** | Semantic / domain validation failure. | Request is well-formed JSON, but business rules fail. |
| **429 Too Many Requests** | Rate limit exceeded. | Must include `Retry-After` header. |
| **500 Internal Server Error** | Unexpected unhandled server panic or crash. | Never expose stack traces in production payloads. |
| **502 / 503 / 504** | Downstream dependency failures / timeouts. | Transient gateway errors suitable for client retry. |

---

## 3. Standard Error Envelope (RFC 7807 Problem Details)
Always return error responses using the RFC 7807 standard format (`application/problem+json`):

```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The request payload failed domain validation rules.",
  "instance": "/orders/123/items",
  "invalid_params": [
    {
      "name": "quantity",
      "reason": "Must be greater than zero."
    }
  ]
}
```

---

## 4. Pagination & Query Standards
- **Cursor/Keyset Pagination (Recommended for Scale)**:
  - Query: `GET /orders?limit=20&cursor=eyJpZCI6MTAxfQ==`
  - Response:
    ```json
    {
      "data": [...],
      "pagination": {
        "limit": 20,
        "next_cursor": "eyJpZCI6MTIxfQ==",
        "has_more": true
      }
    }
    ```
- **Avoid Deep Offset Pagination**: `OFFSET 100000` forces the database to scan and discard 100,000 rows. Use keyset pagination (`WHERE id > :last_seen_id ORDER BY id ASC LIMIT 20`).
- **Filtering & Sorting**:
  - Filter: `GET /orders?status=shipped&created_after=2026-01-01T00:00:00Z`
  - Sort: `GET /orders?sort=-created_at,total_amount` (`-` prefix denotes descending order).

---

## 5. API Versioning & Evolution
- **URI Path Versioning**: Use `/v1/`, `/v2/` at the route root.
- **Additive Changes Only**:
  - ✅ Adding new optional fields to a request.
  - ✅ Adding new fields to a response.
  - ❌ Renaming or deleting an existing field.
  - ❌ Changing a field's data type.
  - ❌ Changing validation rules from optional to required.
- **Deprecation**: Return a `Deprecation: @<timestamp>` and `Sunset: <date>` HTTP header before retiring an endpoint.

---

## 6. Language & Framework Idioms

* **Go**:
  * Define explicit request/response structs with `json:"field_name"` tags.
  * Use strict decoding (`json.NewDecoder(r.Body).DisallowUnknownFields()`) to catch client typos.
* **PHP (Symfony)**:
  * Use Symfony Serializer / API Platform DTOs with typed validation attributes (`#[Assert\NotBlank]`, `#[Assert\Positive]`).
  * Return Symfony's built-in `JsonResponse` or custom RFC 7807 response value objects.
* **Python (FastAPI)**:
  * Strict Pydantic models for request (`Body`) and response (`response_model`).
  * Custom exception handler for `RequestValidationError` mapping directly to RFC 7807 problem details.
