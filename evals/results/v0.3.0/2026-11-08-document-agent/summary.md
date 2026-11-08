# Document Agent (Microsoft Foundry) — v0.3.0 step 3

Date: 2026-11-08. Set-up and script: [`foundry/README.md`](../../../../foundry/README.md).

## Build

| # | Step | Result |
|---|---|---|
| B1 | Foundry → `proj-loandesk` → Agents → **Build an agent**: `loandesk-document-agent`, Text, Microsoft Copilot harness off | Created, version 1 |
| B2 | Model `gpt-4.1-mini`; instructions from `foundry/document-agent-instructions.md` | Done |
| B3 | Web search, which the portal adds to a new agent, removed; `required-documents.md` uploaded with **Upload files** (File search, new vector index, status *Completed*) | Saved as version 2 |

## Playground

| # | Question | Answer | Pass |
|---|---|---|---|
| P1 | "I am a sole proprietor and I have my bank statements and ID. What else do I need?" | Completed application, guarantor's ID, how the loan will be used, commercial registration certificate, PND.90 for the last 2 years, house registration; upload through the LoanDesk assistant; `Source: required-documents.md` with a citation. 3 s, 2,138 tokens | Yes |

The guarantor's ID stays on the list: "ID" in the question does not say whose ID it is, and the checklist
asks for the guarantor's. Acceptable; the agent errs on the side of listing a document.

## Activity protocol

`foundry/activity_endpoint.py` from Cloud Shell, downloaded at a pinned commit and checked by SHA-256.

| # | Run | Result |
|---|---|---|
| A1 | First version, show only | The agent returns protocols twice, as the list `protocols` and the map `protocol_configuration`, plus the read-only `publish_approval_status`. The script added `activity` to the list only and would have sent the read-only field back. **Not applied**; script fixed (`35d3175`) and a test added with this shape |
| A2 | Fixed version, show only | Sends only `protocols` (responses, activity), `protocol_configuration` (responses, activity) and `authorization_schemes` (Entra, BotServiceRbac) |
| A3 | `--apply` | After the change the agent shows activity and responses in both fields, Entra and BotServiceRbac; `version_selector` unchanged. "Done: the Activity protocol is on." |
| A4 | `GET …/agents/loandesk-document-agent` | `id` and `name` are both `loandesk-document-agent`: that is the **Agent Id** Copilot Studio asks for. The GUIDs on the Details page are the agent's Entra identity and blueprint, not its ID |

Two Cloud Shell sessions restarted between commands and lost the `PROJECT_ENDPOINT` variable: the script
then stops with "must start with https://", and `az rest` with an empty base URL goes to Azure Resource
Manager and returns *MissingSubscription*. Set the variable again in each new session.

## Connection in Copilot Studio

LoanDesk Apply Agent → **Agents** → **Add** → Microsoft Foundry: new connection *LoanDesk Document Agent*
(Microsoft Entra ID User Login, the project endpoint), then Name, Description (when to use it and when not:
not eligibility, rates, credit scores, status or applying) and Agent Id `loandesk-document-agent`. The
connected agent shows *Azure AI Foundry Agent Service, external agent activity protocol*, Enabled.

## Test pane

| # | Session | Message | Handled by | Answer | Pass |
|---|---|---|---|---|---|
| D1 | New | "I am a sole proprietor and I have my bank statements and ID. What else do I need?" | **LoanDesk Document Agent** (9.0 s) | Same six documents as P1, "You already have bank statements and ID", Source line | Yes |
| D2 | Same as D1 | "What is the interest rate for the SME loan?" | **Rates** topic | Rate table from `rates-and-fees.md` | Yes (routing) |
| D3 | Same as D1 | "What documents do I need to send?" | Document Agent (4.7 s) | Answered for a sole proprietor: the conversation so far reaches the Foundry agent | Not a valid test |
| D3a | New | "What documents do I need to send?" | No tool in the activity map | Asks for the business type and offers the three types | Yes |
| D3b | Same as D3a | "A limited company. I don't have any documents yet." | **LoanDesk Document Agent** (7.1 s) | All four "All businesses" documents and all five limited-company documents, with "last 3 months", "last 2 years", "if VAT-registered" and "if the articles require one"; Source line | Yes |

## Lessons

- **The Agent Id of a new Foundry agent is its name.** The portal's Details page shows the Entra agent
  identity and blueprint GUIDs, which are not it; `GET /agents/<name>` returns `id` = name.
- **Read before you write.** The show-only run caught that the service keeps protocols in two fields; a
  blind PATCH would have left the map without Activity.
- **The conversation reaches the connected agent.** In D3 the Foundry agent knew the business type from
  earlier turns. Test each routing case in a new session.
- **The orchestrator may ask the follow-up question itself.** In D3a no tool ran; the Apply Agent asked for
  the business type and called the Document Agent only once it had it (D3b).
- **Costs.** Each delegated turn is a Copilot Studio turn (Copilot Credits) plus Foundry tokens for the
  agent and its file search; the vector index holds one 2.8 KB file. Check the budget after step 4.
