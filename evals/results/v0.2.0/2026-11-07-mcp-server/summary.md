# Application Status MCP server — v0.2.0 step 6

Date: 2026-11-07. Function app `func-loandesk-mcp-dev` (Flex Consumption, Python 3.14, Southeast Asia, own
storage account `stloandeskmcp`, user-assigned identity `func-loandesk-mcp-dev-uami`, telemetry to
`appi-loandesk-dev`), deployed from Cloud Shell with a remote build from branch `v0.2.0-step6-mcp-server`.

## Dataverse access

- Security role **LoanDesk Status Reader**, created inside solution LoanDesk: Loan Application **Read =
  Organization**, every other privilege on it None; *App Opener privileges* left off (least privilege).
- The managed identity added as an **application user** in `LoanDesk-Dev` (business unit `loandesk-dev`)
  with that role only.
- App settings `DATAVERSE_URL` and `DATAVERSE_CLIENT_ID` set from the CLI (values not recorded here).

## MCP checks (curl from Cloud Shell, `mcp_extension` system key in a shell variable)

| # | Call | Expected | Result |
|---|---|---|---|
| M1 | `initialize` | HTTP 200, server *LoanDesk Application Status* 0.2.0 | Pass (Streamable HTTP, answer as an SSE `message` event, `Mcp-Session-Id` header) |
| M2 | `tools/call` LDK-000004 with its contact e-mail | found, Approved, 2026-11-06 | First run: found, but status "Unknown". Pass after the fix (`bffa940`) |
| M3 | `tools/call` LDK-000004 with another e-mail | found = false, the neutral "no match" message | Pass |

The function list shows one function, `get_application_status`. Unit tests: 10/10.

Fix for M2: the code mapped numeric choice values (852190000 and up) to labels, and the values in the
environment are different. The query now sends `Prefer: odata.include-annotations=
"OData.Community.Display.V1.FormattedValue"` and uses the label Dataverse returns, so the numbers no longer
matter. Lesson: do not hard-code choice values that were not read from the environment.
