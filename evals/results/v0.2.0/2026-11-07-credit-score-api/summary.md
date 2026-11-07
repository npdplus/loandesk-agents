# Credit Score API — v0.2.0 step 5

Date: 2026-11-07. Function app `func-loandesk-credit-dev` (Flex Consumption, Python 3.14, Southeast Asia),
deployed from Azure Cloud Shell with `az functionapp deployment source config-zip --build-remote true`
from branch `v0.2.0-step5-credit-api` at `3e407a8`. Deployment succeeded with basic authentication off.

## API checks (curl from Cloud Shell, key read into a shell variable and never printed)

| # | Request | Expected | Result |
|---|---|---|---|
| A1 | `BIZ-100001` with key | 200, score 881 | Pass |
| A2 | `BIZ-100009` with key | 200, score 659 | Pass |
| A3 | `BIZ-100002` with key | 200, score 414 | Pass |
| A4 | `BIZ-000000` with key | 404, `NoCreditFile` | Pass |
| A5 | `AB` with key | 400, `InvalidBusinessId` | Pass |
| A6 | `BIZ-100001` without key | 401 | Pass |

The function list shows one function, `credit_score`. Unit tests: 9/9 pass locally.

## Custom connector *LoanDesk Credit Score*

Created inside solution LoanDesk from `api/openapi/credit-score.swagger.json` (pasted into the Swagger
editor). Host `@environmentVariables("ldk_CreditApiHost")`, base URL `/api`; security API key, label
*Function key*, header `x-functions-key`. The key is stored only in the connection.

| # | Check | Expected | Result |
|---|---|---|---|
| K1 | Test tab, `GetCreditScore` with `BIZ-100001` | 200, score 881 | Pass (host read from the environment variable) |

Schema validation warned that `checkedAt` is "string undefined" rather than "string date-time". The value is
ISO 8601 UTC (`2026-11-07T09:20:34Z`); the warning does not stop the action.

## Staff agent with the connector as a tool

Tool *Get credit score* added to **LoanDesk Staff Agent** (not the customer agent: the manual keeps scores
and bands from customers). Instructions: the knowledge-only rule now covers rules, rates and documents; a new
rule says when to call the tool, to call the score a mock, to handle "no credit file" and invalid IDs, to
explain the score from the decision guide and to add "Credit Score API" to the Source line. Preview run
used 9 credits.

| # | Question | Expected | Result |
|---|---|---|---|
| C1 | "What is the credit score for BIZ-100009, and what does the decision guide say for that score?" | 659, called a mock; 600–699 rows of the decision guide; no recommendation; reminder not to share; Source line | Pass. Also quoted the four-eyes rule and the DSCR formula, said it has no DSCR, and ended "Source: credit-manual-internal.md, Credit Score API" |
| C2 | "Credit score for BIZ-000000?" | Says there is no credit file | Pass. The test pane marks the call "Failed to use tool … 404", but the agent read the error and answered correctly |

C1 listed D02 and D03 as the decline codes; for a score of 600–699 that fails only on DSCR, D03 is the one
that applies. A small wording issue, not a wrong figure.

## REST tool on the Apply Agent

REST API tool **LoanDesk Credit Score REST** (operation *Get credit score REST*), created in Copilot Studio
from a local copy of the OpenAPI file with the real host (not committed), solution LoanDesk, API key auth
(`x-functions-key`, header), connection *LoanDesk Credit Score REST - maker*. Tool settings: only when
referenced by topics or agents; do not ask the end user; maker-provided credentials; don't respond.

The Apply topic calls it between the application card and the Submit Application flow: input
`Topic.businessId`; outputs `score` to `Topic.creditScore` and `businessId` to `Topic.creditBusinessId`
(so the card's variable is not overwritten). New Dataverse column **Credit score** (`ldk_Creditscore`,
whole number 300–900). The flow has a ninth, optional input `CreditScore` (shown in the topic under
*Advanced inputs*), writes it to the row and adds "Credit score (mock, staff only)" to the approval
details.

| # | Run | Expected | Result |
|---|---|---|---|
| R1 | Apply with `BIZ-100009` | Customer message without a score; row and approval show 659 | Pass: LDK-000008, Credit score 659, approval details show 659 |
| R2 | Apply with `BIZ-000000` | Shows whether a 404 stops the application | Topic stopped: "The connector 'LoanDesk Credit Score REST' returned an HTTP error with code 404 … ConnectorRequestFailure"; no row created |

R2 is the reason for the next part: a tool node in a topic has no error handling (its menu has only
Rename, Delete and New comment), so a business with no credit file, a bad ID or an API outage would stop
the customer's application. The Send HTTP request node has *Continue on error*.

## Send HTTP request with a Key Vault secret

- Key Vault `kv-loandesk-dev` (Azure RBAC, 7-day soft delete), created from Cloud Shell after registering
  the `Microsoft.PowerPlatform` resource provider. Key Vault Secrets Officer for the maker; Key Vault
  Secrets User for Dataverse (app ID `00000007-0000-0000-c000-000000000000`) and for *Microsoft Copilot
  Studio Service*.
- A separate function key `copilot-topic` was created for the topic and stored as secret `credit-api-key`
  with the tag `AllowedEnvironments` = the `LoanDesk-Dev` environment ID. The key went from the CLI into a
  shell variable and into the vault without being printed. (`az functionapp function keys set` redacts the
  value in current CLI versions, so it was read back with `keys list`.)
- Environment variable **Credit API key** (`ldk_CreditApiKey`), data type Secret, store Azure Key Vault,
  reference as the current value. It saved at once, so the read permission was in place.
- Apply topic: **HTTP Request** node, GET
  `"https://" & Env.ldk_CreditApiHost & "/api/credit-score?businessId=" & EncodeUrl(Topic.businessId)`,
  header `x-functions-key` = `Env.ldk_CreditApiKey`, timeout 10 s, response schema from a sample response
  into `Topic.creditResponse`, error handling *Continue on error* with `Topic.httpStatus` and
  `Topic.httpError`. Then *Set variable* `Topic.creditScore = Topic.creditResponse.score`, which feeds the
  flow's optional `CreditScore` input. The tool node was deleted.

| # | Run | Expected | Result |
|---|---|---|---|
| R3 | Apply with `BIZ-100002` | Score 414 in the approval, not in the customer message | Pass: LDK-000009, approval shows 414 |
| R4a | Apply with `BIZ-000000` | Application goes on without a score | Fail: the topic went on (Send HTTP worked), but the flow's *Add a new row* failed with "property 'number_4' doesn't exist". The error branch told the customer to contact the Lending Centre |
| R4 | Same, after the fix | Row created with an empty score; approval says "not available" | Pass: LDK-000010, Credit score empty, approval "Credit score (mock, staff only): not available" |

Fix for R4a: when the optional input is empty the agent does not send it at all, and the token the designer
inserts reads `triggerBody()['number_4']`, which fails on a missing property. The row now uses
`triggerBody()?['number_4']` and the approval uses
`if(empty(triggerBody()?['number_4']), 'not available', string(triggerBody()?['number_4']))`. Lesson: use
`?[...]` for every optional flow input.

## Notes

- The Azure CLI warns that `az functionapp function keys list` shows secrets. The key went into a shell
  variable in an ephemeral Cloud Shell session only.
- `az functionapp show` returned `null` for `state` and `functionAppConfig.runtime` on this Flex
  Consumption app; `az resource show --resource-type Microsoft.Web/sites` with `properties.state` and
  `properties.functionAppConfig.runtime` returned `Running` and Python 3.14.
- The portal defaulted to Python 3.14 and a new Application Insights resource; the existing
  `appi-loandesk-dev` was chosen instead, so the 0.1 GB daily cap applies.
