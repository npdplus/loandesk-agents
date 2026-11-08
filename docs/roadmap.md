# Roadmap

Three versions. Each one ends with something that works and can be shown. Later versions are a bonus: by the
end of v0.2.0 the project already practises about three quarters of the AB-620 skills (32 of 44).

Coverage counts the 44 skill lines of the AB-620 study guide (updated 2026-10-16); see
[ab-620-coverage.md](ab-620-coverage.md).

## v0.1.0 — RAG core

**Goal:** a customer agent and a staff agent answer questions about the SME Working Capital Loan from Contoso
Bank's documents, name their sources, and decline what they should not answer.

- Knowledge: Azure AI Search indexes over the policy library, one per audience, reached through Foundry IQ
  knowledge bases and an MCP tool
- Responsible AI in the instructions: AI disclosure, hand-off to a person, no decisions, no internal content
  for customers
- ALM from day one: one solution, environment variables, solution exported and unpacked into `solution/`
- Evaluation: the first test set (30 questions), run in the Copilot Studio Evaluate tab
- Tested in the Preview pane: the maker's trial licence cannot publish (decision D7)

**Done when:** the test set passes at the agreed rate (set in the v0.1.0 plan), answers name sources, the
solution is in the repository, and the README shows screenshots.

**Coverage:** 11 of 44 skill lines (re-scoped 2026-11-05: topics moved to v0.2.0; 2026-11-06: identity and
channel planning moved to v0.3.0).

Detailed plan: [v0.1.0-plan.md](v0.1.0-plan.md).

## v0.2.0 — Workflow and tools

**Goal:** a business can apply, a credit officer decides, and the agent calls other systems.

- Dataverse table Loan Application
- Agent flow Submit Application: input and output parameters, approval by a credit officer (human in the
  loop), error handling, run monitoring
- Topics call the flow and tools; Send HTTP request
- Tools: the Application Status MCP server, the Credit Score API as a custom connector and as a REST tool,
  a Power Platform connector (Outlook or Teams notification)
- Reusable components shared by the agents
- Application Insights telemetry
- Moved from v0.1.0: topics (generative answers node, custom prompt, topic-level knowledge, variables,
  eligibility adaptive card)
- Moved on to v0.3.0 (2026-11-06): channels, Entra ID sign-in, content moderation and the SharePoint knowledge
  source, because the maker's trial cannot publish

**Coverage:** 21 more, 32 of 44 (73 %).

**Done 2026-11-08** (release `v0.2.0`, solution 0.2.0.1): Evaluate 8/8 staff and 29/29 customer, with every
v0.1.0 question still passing.

Detailed plan: [v0.2.0-plan.md](v0.2.0-plan.md).

## v0.3.0 — Multi-agent and lifecycle

**Goal:** a Front Desk agent routes requests to specialist agents, and the solution moves from Dev to Test.

- Front Desk Agent orchestrates the Policy Agent (as a connected or child agent) and the Document Agent
  (Microsoft Foundry)
- Generative answers with Azure AI Search through Foundry; a model from the Foundry model catalog for a
  custom prompt
- A Copilot connector as a knowledge source
- Power Platform Pipelines from `LoanDesk-Dev` to `LoanDesk-Test`, with the test set run after deployment
- Study notes for computer use, Fabric data agents and A2A
- From v0.2.0: web and Teams channels, Entra ID sign-in for staff, content moderation review, SharePoint
  knowledge, *Needs information* when an approval fails (needs a licence that can publish)

**Coverage:** 9 more, 41 of 44 (93 %), if channels, identity and connected agents can be published (decision
D15 in the plan); otherwise 37 or 38. The last 3 are study only.

Detailed plan: [v0.3.0-plan.md](v0.3.0-plan.md).

## After v0.3.0

- Write the architecture as a one-page decision record per major choice (preparation for AB-100).
- Record a three-minute demo video for each version.
