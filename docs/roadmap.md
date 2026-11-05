# Roadmap

Three versions. Each one ends with something that works and can be shown. Later versions are a bonus: by the
end of v0.2.0 the project already practises about three quarters of the AB-620 skills.

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

**Coverage:** 13 of 44 skill lines (re-scoped 2026-11-05; topics moved to v0.2.0).

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
  eligibility adaptive card), the SharePoint knowledge source, the web page and Teams channels with Entra ID
  sign-in for staff, content moderation settings

**Coverage:** 21 more, 34 of 44 (77 %).

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

**Coverage:** 7 more, 41 of 44 (93 %). The last 3 are study only.

## After v0.3.0

- Write the architecture as a one-page decision record per major choice (preparation for AB-100).
- Record a three-minute demo video for each version.
