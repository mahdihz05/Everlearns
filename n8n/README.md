# n8n Orchestration Foundation

This directory contains the n8n workflows for Content App V2 orchestration. n8n serves purely as an execution and orchestration layer, relying entirely on Django for core business data, settings, and final state persistence.

## Workflow Imports

To deploy these workflows to an n8n instance:

1. Use the n8n UI "Import from File" feature, or use the n8n CLI to bulk-import files from `workflows/`.
2. Ensure you are using n8n version `1.0.0` or higher to support modern nodes and expression syntax.

## Required Environment Variables / Credentials

Workflows rely on credentials and environment variables instead of hardcoded secrets.
See `.env.example` for details on required environment variables.

For workflows executing subflows, ensure that n8n allows calling local workflows (or the specific workflow IDs match after import).

## Required Django Endpoints

n8n expects Django to provide a stable Callback URL to report results. Standard pattern:
- `POST https://<DJANGO_HOST>/api/v1/n8n/callback/`

Payload structure provided by n8n:
```json
{
  "correlationId": "string",
  "status": "success|failed",
  "result": {},
  "errorDetails": "string"
}
```

## Known Missing Integrations / Assumptions

- Text Engine & Visual Engine integrations currently point to assumed proxy URLs defined in env variables. If those engines are absent on the deployment environment, n8n will hit network errors and utilize the retry/failure contract.
- Telegram Publishing routes payload formats matching the existing Django message models, abstracting the exact API call behind standard HTTP nodes until specific Telegram n8n credentials are standardized.
- The `agent-tools-` workflows are placeholders waiting for concrete API specifications from the Agent scope.
