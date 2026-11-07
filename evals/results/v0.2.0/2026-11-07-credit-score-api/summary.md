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

## Notes

- The Azure CLI warns that `az functionapp function keys list` shows secrets. The key went into a shell
  variable in an ephemeral Cloud Shell session only.
- `az functionapp show` returned `null` for `state` and `functionAppConfig.runtime` on this Flex
  Consumption app; `az resource show --resource-type Microsoft.Web/sites` with `properties.state` and
  `properties.functionAppConfig.runtime` returned `Running` and Python 3.14.
- The portal defaulted to Python 3.14 and a new Application Insights resource; the existing
  `appi-loandesk-dev` was chosen instead, so the 0.1 GB daily cap applies.
