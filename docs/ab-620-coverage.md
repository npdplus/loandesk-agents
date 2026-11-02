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
| Plan integration with enterprise systems | Dataverse, Credit Score API, MCP server | 0.2.0 | Planned |
| Plan identity strategy | Anonymous web channel; Entra ID for the Teams staff channel | 0.1.0 | Planned |
| Plan channels and deployment | Web test page and Teams | 0.1.0 | Planned |
| Plan responsible AI strategy | AI disclosure, hand-off, content moderation, no AI decisions | 0.1.0 | Planned |
| Evaluate security and governance considerations | Separate knowledge for customer and staff; governance table in the architecture | 0.1.0 | Planned |
| Plan reusable agent components | Shared topics and flows used by more than one agent | 0.2.0 | Planned |
| Design agents for internal or external audiences | Customer agent and staff agent | 0.1.0 | Planned |

### Create and monitor agent flows in Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create an agent flow | Submit Application | 0.2.0 | Planned |
| Create a human-in-the-loop agent flow | Credit officer approval step | 0.2.0 | Planned |
| Configure actions and connectors | Dataverse and Outlook or Teams actions | 0.2.0 | Planned |
| Monitor agent flows | Flow run history | 0.2.0 | Planned |
| Add input and output parameters | Application details in; application number and status out | 0.2.0 | Planned |
| Implement error handling in agent flows | Retry and a failure message when the API is down | 0.2.0 | Planned |

### Configure topics

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Add agent flows to a topic | Apply topic calls Submit Application | 0.2.0 | Planned |
| Configure agent response formatting | Answers with headings, lists and citations | 0.1.0 | Planned |
| Add tools to a topic | Check Status topic calls the MCP tool | 0.2.0 | Planned |
| Configure advanced agent responses with custom prompts | Plain-language explanation of the eligibility result | 0.1.0 | Planned |
| Configure advanced agent responses with custom knowledge sources | Topic-level knowledge for the rate table | 0.1.0 | Planned |
| Configure advanced agent responses with API and Send HTTP requests | Credit Score API call | 0.2.0 | Planned |
| Configure generative answers node | Policy questions | 0.1.0 | Planned |
| Configure adaptive cards | Eligibility form and result card | 0.1.0 | Planned |
| Manage variables | Eligibility inputs, global variables for the channel | 0.1.0 | Planned |

## 2. Integrate and extend agents in Copilot Studio (40–45 %)

### Connect to enterprise knowledge sources

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Connect to Copilot connectors | A Copilot connector as an extra knowledge source | 0.3.0 | Planned |
| Connect to Microsoft Power Platform connectors | Dataverse or Outlook connector | 0.2.0 | Planned |
| Connect to Azure AI Search | `loan-policy-public` and `loan-policy-staff` (indexes built; connection to the agents pending) | 0.1.0 | Planned |

### Add tools to agents

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Configure and monitor computer use for an agent | Notes only | — | Study |
| Configure MCP tools | Application Status MCP server | 0.2.0 | Planned |
| Add a tool by using an existing custom connector | Credit Score API connector | 0.2.0 | Planned |
| Add REST APIs to an agent | Credit Score API as a REST tool | 0.2.0 | Planned |

### Configure multi-agent collaboration from Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Design multi-agent solutions in Copilot Studio | Front Desk with specialist agents | 0.3.0 | Planned |
| Integrate a Foundry agent | Document Agent | 0.3.0 | Planned |
| Integrate an existing agent in Copilot Studio | Policy Agent connected to Front Desk | 0.3.0 | Planned |
| Integrate a Fabric data agent | Notes only | — | Study |
| Create a multi-agent solution by using A2A protocol | Notes only | — | Study |

### Integrate agents with Azure

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Configure generative answers by using Azure AI Search with Foundry | Policy answers through Foundry | 0.3.0 | Planned |
| Configure custom prompts to use the Foundry model catalog | Summary prompt on a catalog model | 0.3.0 | Planned |
| Monitor agents by using Application Insights | Telemetry from all agents | 0.2.0 | Planned |

## 3. Test and manage agents (20–25 %)

### Evaluate agent performance

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create a test set | `evals/` | 0.1.0 | Planned |
| Choose an evaluation method | Exact facts, citation present, refusal expected | 0.1.0 | Planned |
| Review test results | Results stored in `evals/results/` | 0.1.0 | Planned |

### Implement application lifecycle management (ALM) for agents in Copilot Studio

| Skill | Where in LoanDesk | Version | Status |
|---|---|---|---|
| Create a solution | LoanDesk solution | 0.1.0 | Planned |
| Add existing agents to a solution | Agents built in the solution or added to it | 0.1.0 | Planned |
| Create and use environment variables | `ldk_SearchIndexPublic`, `ldk_SearchIndexStaff` and later variables | 0.1.0 | Planned |
| Implement and extend Microsoft Power Platform Pipelines | Dev to Test | 0.3.0 | Planned |

## Totals

| Version | New skill lines | Running total | Share of 44 |
|---|---|---|---|
| 0.1.0 | 18 | 18 | 41 % |
| 0.2.0 | 16 | 34 | 77 % |
| 0.3.0 | 7 | 41 | 93 % |
| Study only | 3 | 44 | 100 % read |
