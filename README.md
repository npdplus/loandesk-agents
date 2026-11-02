# LoanDesk Agents

A demo AI agent loan desk for **Contoso Bank**, a fictional bank. It is built with Microsoft Copilot Studio,
Azure AI Search, Microsoft Foundry and Dataverse.

A small business asks about a working-capital loan, checks whether it qualifies, and applies. The agents
answer from the bank's policy documents (RAG), pre-screen the application, and hand it to a credit officer.
**A person makes every decision; the AI never approves a loan.**

> **Status:** v0.1.0 in progress. The environments are ready and the knowledge documents are written; the
> agents are not built yet. See [the roadmap](docs/roadmap.md) and [the v0.1.0 plan](docs/v0.1.0-plan.md).
>
> Everything here is fictional: Contoso Bank, its products, rates, policies, customers and applications.
> This is a learning and portfolio project, not a banking product.

## Why this project exists

- To learn every part of an enterprise agent solution, end to end, on a system small enough to finish.
- To cover the scope of the Microsoft exam **AB-620: Designing and Building Integrated AI Agent Solutions in
  Copilot Studio**. The [coverage map](docs/ab-620-coverage.md) links each skill to the part of this system
  that practises it.
- To show how an AI agent can follow governance rules a bank needs: human oversight, explainable answers
  with sources, tests before and after a change, and monitoring.

## What it does

```text
Customer (web) ──┐                    ┌── Policy Agent    answers from policy documents (RAG)
Staff (Teams) ───┴──► Front Desk ─────┼── Document Agent  checks application documents (Foundry)
                      Agent           ├── MCP tool        reads application status (Dataverse)
                      (orchestrator)  ├── Credit API      mock credit score (custom connector / REST)
                                      └── Agent flow      submit ──► credit officer approves or rejects
```

| Version | Theme | What works at the end |
|---|---|---|
| v0.1.0 | RAG core | The Policy Agent answers loan questions from the bank's documents, with sources, on a web page and in Teams |
| v0.2.0 | Workflow and tools | A business can apply; a credit officer approves or rejects; agents call an MCP tool and a REST API |
| v0.3.0 | Multi-agent and lifecycle | A Front Desk agent routes work to specialist agents; the solution moves from Dev to Test with Pipelines |

## Built with

| Tool | Used for |
|---|---|
| Microsoft Copilot Studio | Agents, topics, agent flows, tools, evaluation |
| Microsoft Dataverse | Loan applications, environment variables, solution packaging |
| SharePoint Online and Microsoft Teams | Short guides as a knowledge source; the staff channel |
| Azure AI Search | Retrieval over the full policy library |
| Microsoft Foundry | Models for custom prompts; the Document Agent |
| Azure Functions (Python) | The mock credit-score API and the MCP server |
| Application Insights | Agent telemetry |
| Power Platform Pipelines and Power Platform CLI | Dev to Test deployment; the solution as source code |
| Copilot Studio Kit and PromptDiff | Batch tests and regression checks of agent answers |

## Repository layout

```text
solution/     Copilot Studio agents and Dataverse components (unpacked solution)
api/          Azure Functions: mock credit-score API (v0.2.0)
mcp-server/   MCP server that reads application status (v0.2.0)
knowledge/    Contoso Bank's fictional policy and product documents
evals/        Test sets and results
docs/         Architecture, roadmap, AB-620 coverage, version plans, references
```

## Documents

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [AB-620 coverage map](docs/ab-620-coverage.md)
- [v0.1.0 plan](docs/v0.1.0-plan.md)
- [References and upstream samples](docs/references.md)

## Rules for this repository

- **Fictional data only.** No real bank, customer, person or document.
- **No secrets.** No keys, connection strings, tenant IDs or environment URLs in commits. Local settings stay
  in `.env` and `local.settings.json`, which Git ignores.
- **Credit for borrowed work.** Code taken from other projects is listed in
  [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) with its source and licence.

## Licence

[MIT](LICENSE) © 2026 NPD PLUS
