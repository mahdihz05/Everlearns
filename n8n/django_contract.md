# Django ↔ n8n Contract

This document defines the strict boundaries and integration contracts between Django and n8n in Content App V2.

## Boundary Definitions
- **Django** is the authoritative source for business logic, users, content data, configuration, permissions, and primary state.
- **n8n** is strictly an orchestration layer. It handles execution steps, API chaining, async long-running processes, and retries. n8n must not own authoritative business data.

## 1. Authenticated Workflow Invocation
- Django triggers n8n workflows via n8n Webhook nodes.
- Webhooks must be protected (e.g., using a shared secret token in headers: `Authorization: Bearer <N8N_WEBHOOK_SECRET>`).

## 2. Structured Input
- Django sends a JSON payload to n8n.
- Required base fields:
  ```json
  {
    "correlationId": "uuid-v4",
    "action": "generate-text",
    "callbackUrl": "https://django-api.example.com/api/v1/n8n/callback/",
    "payload": { ... }
  }
  ```

## 3. Structured Output (Callback/Status)
- n8n reports progress, completion, or failure back to Django's `callbackUrl`.
- Callback Payload Format:
  ```json
  {
    "correlationId": "uuid-v4",
    "status": "success | failed | processing",
    "result": { ... },
    "errorDetails": "Optional error string if failed"
  }
  ```
- Authentication for callbacks: n8n must include a valid token in the headers when calling Django: `Authorization: Bearer <DJANGO_API_TOKEN>`.

## 4. Retries and Idempotency
- **Idempotency:** Workflows should be designed to be idempotent where possible. The `correlationId` can be used by Django to ignore duplicate success callbacks.
- **Retries:** n8n will handle transient API failures internally (e.g., HTTP nodes configured to retry on 5xx or 429 errors). If max retries are exceeded, n8n will send a `failed` status back to Django.

## 5. Timeout Behavior
- n8n is responsible for managing timeouts on external API calls.
- If an external AI provider times out after all retries, n8n must gracefully terminate and notify Django with a failure status.

## 6. Error Reporting
- All unexpected errors must be caught by an error handler workflow (or error trigger).
- The error handler ensures Django always receives a final status for a `correlationId`.
