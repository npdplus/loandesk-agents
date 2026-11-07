# Credit Score API (mock)

An Azure Function in Python that returns a **made-up** credit score for a fictional business ID. The agents
call it through a custom connector and as a REST tool. Built in v0.2.0, step 5.

The score comes from a hash of the business ID, so the same ID always gets the same score and nothing is
stored. It is not a real credit check.

## Endpoint

`GET /api/credit-score?businessId=BIZ-100001` with the function key in the `x-functions-key` header.

| Business ID | Result | Use it to test |
|---|---|---|
| `BIZ-100001` | 200, score 881 | Score of 700 or more |
| `BIZ-100009` | 200, score 659 | Score of 600 to 699 |
| `BIZ-100002` | 200, score 414 | Score below 600 |
| `BIZ-000000` | 404, `NoCreditFile` | No credit file |
| `AB` | 400, `InvalidBusinessId` | Bad input |

A business ID is 3 to 20 letters, digits or hyphens. Lower case is accepted and returned upper-cased.

The response has `businessId`, `score`, `scoreMin` (300), `scoreMax` (900), `checkedAt` (UTC), `source`
and `mock` (always `true`). It never returns the decision bands: those are in the internal credit manual
and must not reach customers.

## Files

| File | What it is |
|---|---|
| `function_app.py` | The HTTP function (Python v2 programming model), function-key auth |
| `scoring.py` | Validation and the mock score |
| `openapi/credit-score.swagger.json` | OpenAPI 2.0 definition for the custom connector and the REST tool. Replace the placeholder `host` with the function app's host name when you import it |
| `tests/` | Unit tests |

## Test

```bash
cd api
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python -m unittest discover -s tests
```

## Hosting

Function app `func-loandesk-credit-dev` on the **Flex Consumption** plan in `rg-loandesk-dev` (Southeast
Asia), Python 3.14, 512 MB instances, no always-ready instances, so it bills only per execution, inside the
monthly free grant at this volume. The Linux Consumption plan was not used: it gets no new Python versions
and retires on 30 September 2028.

- **Storage:** its own account, not the one that holds the knowledge documents, so the app cannot reach the
  internal credit manual.
- **Identity:** a user-assigned managed identity reaches host storage, deployment storage and Application
  Insights (`appi-loandesk-dev`), so no connection string sits in the app settings. Basic authentication
  and continuous deployment are off.

## Deploy from Azure Cloud Shell

Flex Consumption has no in-portal code editor, so deploy a package with a remote build (Azure installs the
packages on Linux). In Cloud Shell (Bash, no storage needed):

```bash
git clone --depth 1 https://github.com/npdplus/loandesk-agents.git
cd loandesk-agents/api
zip -r ../api.zip . -x 'tests/*' 'openapi/*' '*.md'
az functionapp deployment source config-zip \
  --resource-group rg-loandesk-dev --name <function-app-name> \
  --src ../api.zip --build-remote true
```

The function key is copied from the portal (**Functions → credit_score → Function keys**) straight into the
connection in Power Platform. It never goes into this repository, a chat or a document. Settings for a local
run stay in `local.settings.json`, which Git ignores.
