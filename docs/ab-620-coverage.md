# AB-620 coverage map

Source: Microsoft Learn, *Study guide for Exam AB-620: Designing and Building Integrated AI Agent Solutions in
Copilot Studio*, skills list updated 2026-10-16. Check the study guide again before booking the exam; Microsoft
updates it.

Status values: **Planned**, **Done** (built and shown in the repository), **Study** (read and write notes, no
build).

## 1. Plan and configure agent solutions (30–35 %)

### Plan an agent solution

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Plan integration with enterprise systems | Dataverse through an agent flow, the Credit Score API through a custom connector, a REST tool and Send HTTP, and Dataverse through an MCP server with a managed identity (decisions D13, D14) | 0.2.0 | Done |
| Plan identity strategy | Anonymous web channel; Entra ID for the Teams staff channel | 0.3.0 | Planned |
| Plan channels and deployment | Web test page and Teams | 0.3.0 | Planned |
| Plan responsible AI strategy | AI disclosure, hand-off, no AI decisions, no internal content for customers (decision D1); content moderation review in 0.3.0 | 0.1.0 | Done |
| Evaluate security and governance considerations | Separate knowledge for customer and staff; governance table in the architecture; keys in connections and Key Vault, least-privilege role for the MCP server (D13, D14) | 0.1.0 | Done |
| Plan reusable agent components | Component collection *LoanDesk shared components* (Talk to a person); shared with the Front Desk agent in 0.3.0 | 0.2.0 | Done |
| Design agents for internal or external audiences | Customer agent and staff agent, each with its own knowledge and tools | 0.1.0 | Done |

### Create and monitor agent flows in Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create an agent flow | Submit Application | 0.2.0 | Done |
| Create a human-in-the-loop agent flow | Credit officer approval step; decision written back | 0.2.0 | Done |
| Configure actions and connectors | Dataverse and Approvals actions; Outlook or Teams later | 0.2.0 | Done |
| Monitor agent flows | Run history used to find and fix a failed run | 0.2.0 | Done |
| Add input and output parameters | Application details in; application number, status and message out | 0.2.0 | Done |
| Implement error handling in agent flows | Run-after branch that answers the agent when the row cannot be saved | 0.2.0 | Done |

### Configure topics

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Add agent flows to a topic | Apply topic calls Submit Application | 0.2.0 | Done |
| Configure agent response formatting | Answers with lists and a `Source:` line (instructions) | 0.1.0 | Done |
| Add tools to a topic | Apply topic called the Credit Score REST tool (R1, later replaced by Send HTTP) | 0.2.0 | Done |
| Configure advanced agent responses with custom prompts | Plain-language explanation of the eligibility result (prompt on GPT-4.1 mini) | 0.2.0 | Done |
| Configure advanced agent responses with custom knowledge sources | Rates topic limited to `rates-and-fees.md` | 0.2.0 | Done |
| Configure advanced agent responses with API and Send HTTP requests | Apply topic fetches the credit score with Send HTTP request: key from a Key Vault secret variable, response schema from a sample, *Continue on error* (decision D13) | 0.2.0 | Done |
| Configure generative answers node | Rates topic | 0.2.0 | Done |
| Configure adaptive cards | Eligibility form; application form | 0.2.0 | Done |
| Manage variables | Card output variables; flow outputs; Power Fx conversion | 0.2.0 | Done |

## 2. Integrate and extend agents in Copilot Studio (40–45 %)

### Connect to enterprise knowledge sources

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Connect to Copilot connectors | Enterprise websites connector over a public glossary, indexed and added to the Front Desk as knowledge; queries fail in this tenant (connector search error), so the answer path is untested | 0.3.0 | Partial |
| Connect to Microsoft Power Platform connectors | Dataverse, Approvals and Office 365 Outlook connectors in the Submit Application flow | 0.2.0 | Done |
| Connect to Azure AI Search | Foundry IQ knowledge bases over `loan-policy-public` and `loan-policy-staff`, through the Foundry IQ MCP tool (customer agent connected 2026-11-05; decision D8) | 0.1.0 | Done |

### Add tools to agents

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Configure and monitor computer use for an agent | Notes only | — | Study |
| Configure MCP tools | Own MCP server *LoanDesk Application Status* (Azure Functions MCP extension, API key) on the customer agent; Foundry IQ MCP since v0.1.0 | 0.2.0 | Done |
| Add a tool by using an existing custom connector | Custom connector *LoanDesk Credit Score* as a staff agent tool; host from `ldk_CreditApiHost` | 0.2.0 | Done |
| Add REST APIs to an agent | *LoanDesk Credit Score REST* on the Apply Agent, maker credentials, topics only | 0.2.0 | Done |

### Configure multi-agent collaboration from Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Design multi-agent solutions in Copilot Studio | *LoanDesk Front Desk* routes to the Policy child agent, the Foundry Document Agent and four topics; diagram and hand-off rules in architecture §9 | 0.3.0 | Done |
| Integrate a Foundry agent | Foundry prompt agent *LoanDesk Document Agent* (File search over the public checklist), Activity protocol enabled by script, connected to the Apply Agent (preview) | 0.3.0 | Done |
| Integrate an existing agent in Copilot Studio | Policy Agent connected to Front Desk | 0.3.0 | Planned |
| Integrate a Fabric data agent | Notes only | — | Study |
| Create a multi-agent solution by using A2A protocol | Notes only | — | Study |

### Integrate agents with Azure

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Configure generative answers by using Azure AI Search with Foundry | Policy child agent with Azure AI Search `loan-policy-public` as knowledge; questions vectorized by the index's Foundry embedding model (decision D18) | 0.3.0 | Done |
| Configure custom prompts to use the Foundry model catalog | *Explain eligibility result 1* on the Foundry deployment `gpt-4.1-mini` (bring your own model) | 0.3.0 | Done |
| Monitor agents by using Application Insights | Apply Agent telemetry; KQL in `monitoring/queries.kql` (standard harness only) | 0.2.0 | Done |

## 3. Test and manage agents (20–25 %)

### Evaluate agent performance

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create a test set | `evals/v0.1.0-test-set.csv`, imported per agent from `evals/import/` | 0.1.0 | Done |
| Choose an evaluation method | Compare meaning against written expected answers | 0.1.0 | Done |
| Review test results | One failure found, fixed in the instructions and rerun; `evals/results/` | 0.1.0 | Done |

### Implement application lifecycle management (ALM) for agents in Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create a solution | LoanDesk solution | 0.1.0 | Done |
| Add existing agents to a solution | Agents built in the solution or added to it | 0.1.0 | Done |
| Create and use environment variables | `ldk_ApproverEmail` read by the Submit Application flow; `ldk_CreditApiHost` in a custom connector and a topic; secret `ldk_CreditApiKey` from Key Vault | 0.1.0 | Done |
| Implement and extend Microsoft Power Platform Pipelines | Dev to Test | 0.3.0 | Planned |

## Totals

| Version | New skill lines | Running total | Share of 44 |
|---|---|---|---|
| 0.1.0 | 11 | 11 | 25 % |
| 0.2.0 | 21 | 32 | 73 % |
| 0.3.0 | 9 | 41 | 93 % |
| Study only | 3 | 44 | 100 % read |

Re-scoped 2026-11-05: five topic skills moved from v0.1.0 to v0.2.0 (see the v0.1.0 plan). Re-scoped
2026-11-06: identity and channel planning moved to v0.3.0 with step 10, because the trial cannot publish.
Status checked against the repository at the v0.2.0 release (2026-11-08): every 0.1.0 and 0.2.0 line is Done.
