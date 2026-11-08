# Application Status MCP server

A remote MCP server on Azure Functions (Python) with one read-only tool, `get_application_status`, which
returns the status of a loan application. Built in v0.2.0, step 6, with the Azure Functions MCP extension
(MCP tool trigger). It was written from the Microsoft Learn reference; no code was copied from the
`Azure-Samples/remote-mcp-functions-python` sample.

## The tool

| Input | Example | Required |
|---|---|---|
| `applicationNumber` | `LDK-000004` | Yes |
| `contactEmail` | The contact e-mail address on the application | Yes |

Both must match the same row. A wrong e-mail address and an unknown number give the same answer, so trying
numbers reveals nothing. The tool returns only:

```json
{"found": true, "applicationNumber": "LDK-000004", "status": "Approved",
 "lastUpdated": "2026-11-06", "nextStep": "The Lending Centre will contact you about the next steps."}
```

or `{"found": false, "message": "..."}`. It never returns the credit score, amount, decision reason,
business name or who decided.

## How it reaches Dataverse

The function app's user-assigned managed identity is an **application user** in `LoanDesk-Dev` with a
security role that can only **read** Loan Application rows. The function asks for a token for the
environment URL and calls the Web API (`GET .../api/data/v9.2/ldk_loanapplications`, filtered on the
application number after it matches `^LDK-\d{6}$`). It never writes.

App settings (set on the function app, never in this repository):

| Setting | Holds |
|---|---|
| `DATAVERSE_URL` | Environment URL, for example `https://<org>.crm5.dynamics.com` |
| `DATAVERSE_CLIENT_ID` | Client ID of the managed identity that is the application user |

Logs record only the error type when a look-up fails: no application number, e-mail address or token.

## Endpoint and key

- Streamable HTTP at `https://<function-app-host>/runtime/webhooks/mcp` (SSE is not used; Copilot Studio no
  longer supports it).
- The extension requires the **`mcp_extension` system key** in the `x-functions-key` header. The key goes
  straight from the portal or the CLI into the Copilot Studio connection, never into this repository.

## Files

| File | What it is |
|---|---|
| `function_app.py` | The MCP tool trigger and its two properties |
| `status.py` | Input checks, the match rule and the answer (no Azure dependencies) |
| `dataverse.py` | Read-only Web API query |
| `host.json` | MCP server name, version and instructions; system-key authorization |
| `tests/` | Unit tests with a fake store and a mocked Web API |

## Test

```bash
cd mcp-server
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests
```

## Deploy from Azure Cloud Shell

Function app `func-loandesk-mcp-dev`: Flex Consumption, Python 3.14, 512 MB, its own storage account and
managed identity, basic authentication off. Deploy with a remote build, as for the Credit Score API:

```bash
git clone --depth 1 https://github.com/npdplus/loandesk-agents.git
cd loandesk-agents/mcp-server
zip -r ~/mcp.zip . -x 'tests/*' '*.md' '.funcignore'
az functionapp deployment source config-zip \
  --resource-group rg-loandesk-dev --name func-loandesk-mcp-dev \
  --src ~/mcp.zip --build-remote true
```
