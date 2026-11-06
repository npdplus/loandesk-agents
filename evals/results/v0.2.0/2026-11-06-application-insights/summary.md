# Application Insights — 2026-11-06

*LoanDesk Apply Agent* sends telemetry to **appi-loandesk-dev** (workspace-based, on Log Analytics workspace
**log-loandesk-dev**, both in `rg-loandesk-dev`, Southeast Asia). Connected in *Settings → Advanced →
Application Insights* with the connection string, which stays in the agent and the Azure portal only.

Only standard-harness agents support this (Microsoft Learn, *Capture telemetry with Application Insights*), so
the customer and staff agents are not connected.

## Settings

| Option | Value | Why |
|---|---|---|
| Enable logging | On | Messages and events |
| Node execution events | On | One event per node, to see each topic's path |
| Log conversation details | **Off** | No user names or message text in the logs (decision D12) |
| Log sensitive Activity properties | **Off** | Same |
| Log Analytics daily cap | 0.1 GB a day | Cost guard; a demo sends far less |

## Check

One test-pane conversation: a rates question, an eligibility check (rule E3) and "talk to a person". After
about three minutes, `monitoring/queries.kql`:

| Query | Result |
|---|---|
| 1. Event types, last hour | TopicAction 18, BotMessageSend 9, BotMessageReceived 7, TopicStart 6, TopicEnd 6, GenerativeAnswers 1 |
| 2. Topic starts, last hour | ConversationStart 3, Talktoaperson 1, Checkeligibility 1, Rates 1 |

Topic names appear as `ldk_applyagent.topic.<name>`, including *Talk to a person*, which now lives in the
component collection.

## Notes

- The Log Analytics workspace was created first in `rg-loandesk-dev`; the Application Insights wizard
  otherwise offers a new *DefaultWorkspace* in a separate *DefaultResourceGroup-SEA*, outside the budget alert.
- The Logs page opens with the *Observability Agent* chat; switch it off to write KQL.
- Test-pane traffic has `designMode` = `True`; query 3 filters it out once there are real users.
