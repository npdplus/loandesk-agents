# Custom prompt on a Foundry model — v0.3.0 step 2

Date: 2026-11-08. The prompt *Explain eligibility result 1* (used by the **Check eligibility** topic of
*LoanDesk Apply Agent*) now runs on the Foundry deployment `gpt-4.1-mini` in `aif-loandesk-dev-03`
(bring your own model).

## Connecting the model

Prompt editor → **Model** → *Azure AI Foundry Models* → **+** → *Connect a model from Azure AI Foundry*:

| Field | Value |
|---|---|
| Model deployment name | `gpt-4.1-mini` |
| Base model name | `gpt-4.1-mini` |
| Azure model endpoint URL | `https://<resource>.services.ai.azure.com/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2025-01-01-preview` |
| API key | The resource key, pasted into the form only |
| Model description | `LoanDesk Foundry gpt-4.1-mini (Global Standard, 10K TPM)` |
| Test the connection | On |

| # | Endpoint URL tried | Result |
|---|---|---|
| B1 | `…/openai/deployments/gpt-4.1-mini/chat/completions` (no `api-version`) | *Connecting model failed. Resource not found* |
| B2 | The same with `?api-version=2025-01-01-preview` | **Connected** |

The Foundry deployment page shows a Responses API URL (`…/openai/v1/responses`); prompts need the chat
completions URL instead, and Microsoft Learn says the Responses URL also fails with *Resource not found*.

## Prompt editor tests

Same instructions, same sample input (the R2 text of case T1):
`Not eligible as requested. Rule R2: the requested amount is more than 30% of annual revenue. You could ask for up to THB 450,000.`

| # | Model | Output (summary) | Time | Credits | Pass |
|---|---|---|---|---|---|
| P0 | Foundry `gpt-4.1-mini`, **sample data empty** | Generic: "some eligibility criteria were not met"; no rule, no amount | 4,190 ms | 0.2 | — (test set-up error) |
| P1 | Foundry `gpt-4.1-mini` | 3 sentences: over 30 % of annual revenue, could ask for up to THB 450,000, a credit officer makes the final decision | 3,582 ms | 0.2 | Yes |
| P2 | Built-in *Basic GPT-4.1 mini* | Almost word for word the same as P1 | 3,059 ms | 0.2 | Yes |

The prompt was saved with the Foundry model. Its name stayed *Explain eligibility result 1*, and the topic's
Prompt node still points at it.

## Topic tests (test pane, new session each)

| # | Card (years, revenue, amount, term) | Rule message | "In plain words (AI-generated)" | Pass |
|---|---|---|---|---|
| T1 | 2, 1,500,000, 600,000, 24 | R2, up to THB 450,000 | Amount higher than allowed; up to 30 % of revenue, THB 450,000; lowering the request would meet the rule; a credit officer determines approval. No new numbers | Yes |
| T2 | 3, 2,000,000, 500,000, 12 | Eligible to apply (E2, E3, R1, R2, R3) | Meets the pre-check rules; a credit officer reviews and decides. No numbers, no promise of approval | Yes |

Both cases ended with the pre-check disclaimer.

## Did the calls reach Foundry?

Azure portal → `aif-loandesk-dev-03` → Metrics → *Azure OpenAI Requests*, Sum, last 24 hours: **6**. That is
the step 1 playground test, the connection test (B2), P0, P1, T1 and T2. P2 used the built-in model and is
not counted, so the topic's calls went to the Foundry deployment.

## Budget check (steps 1 and 2)

Budget `budget-loandesk-dev` on `rg-loandesk-dev`, USD 10 a month, on 2026-11-08:

| | USD |
|---|---|
| Spent in November (1–8) | 6.78 (67.78 %) |
| Forecast for the month | 36.81 |

Cost analysis by resource and service:

| Source | USD |
|---|---|
| Power Platform billing plan (`microsoft.powerplatform/accounts`, Japan East): Microsoft Copilot Studio | 6.36 |
| The same billing plan: Dataverse | 0.42 |
| Every Azure resource together: both Foundry resources, storage, Key Vault, Log Analytics, AI Search, both function apps | under 0.10 |

The Foundry tokens of steps 1 and 2 cost less than a cent. Almost all of the spend is **Copilot Credits**
on the pay-as-you-go billing plan of `LoanDesk-Dev`: the agents' test sessions, prompts, agent flow runs and
above all the Evaluate runs (the v0.2.0 runs alone used 187 credits). The forecast extends those bursts
across the whole month, so it overstates steady use, but the remaining v0.3.0 steps (multi-agent tests,
Evaluate in `LoanDesk-Test`) will add more credits and the month is likely to pass USD 10.

Note: the budget lives on the resource group, so it does not show on the billing account's Budgets page.

## Lessons

- **Set the sample data before testing a prompt.** With the input empty, the model still answers, but
  generically (P0), which looks like a model problem and is not one.
- **A Foundry model still costs Copilot Credits.** Each prompt run used 0.2 credits with either model; the
  Foundry tokens are billed on top, in Azure. Bring your own model buys a choice of model and Foundry's
  controls (content filters, quota, monitoring), not a lower Copilot Studio bill.
- **The responsible-AI duty moves to us.** The editor reminds that with a Foundry model, content filters and
  other mitigations are set in Foundry (the deployment uses the default guardrails).
- **Fallback:** switching back is one click in the Model menu (*Basic GPT-4.1 mini*), then Save.
