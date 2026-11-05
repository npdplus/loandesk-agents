# Architecture

This is the target design for v0.3.0. Each part is marked with the version that builds it. All data is
fictional.

## 1. Scenario

Contoso Bank offers one product in this demo: the **SME Working Capital Loan**.

- A **customer** (a small business) asks questions on the bank's web page, checks eligibility, and applies.
- A **credit officer** (staff) uses Teams to ask about internal rules, review applications, and decide.
- The AI answers, pre-screens and summarises. **It never approves or rejects.** Every decision is a
  person's, recorded with a reason.

## 2. Components

| Component | What it is | Version |
|---|---|---|
| Policy Agent | Two Copilot Studio agents, *LoanDesk Customer Agent* and *LoanDesk Staff Agent*. Answer from policy documents and name the source (Azure AI Search through Foundry IQ; SharePoint from 0.2.0) | 0.1.0 |
| Eligibility topic | Topic with an adaptive card; checks the basic rules and explains the result | 0.2.0 |
| Submit Application flow | Agent flow: creates the application in Dataverse, asks a credit officer to decide (human in the loop), tells the customer | 0.2.0 |
| Credit Score API | Azure Function (Python) returning a mock score for a fictional business ID; called through a custom connector and as a REST tool | 0.2.0 |
| Application Status MCP server | Azure Function (Python) MCP server with one read-only tool, `get_application_status` | 0.2.0 |
| Front Desk Agent | Orchestrator. Routes each request to the right agent, tool or flow | 0.3.0 |
| Document Agent | Microsoft Foundry agent. Checks that an application has the required documents and summarises them | 0.3.0 |

Study only (no build, because they need extra licences or paid capacity): computer use, a Fabric data
agent, and the A2A protocol. Notes go in `docs/study/`.

## 3. Channels and identity

| Channel | Audience | Sign-in | Knowledge allowed |
|---|---|---|---|
| Web page (demo website or test pane) | Customers | None | Public documents only |
| Microsoft Teams | Credit officers | Microsoft Entra ID | Public and internal documents |

Internal documents (the credit manual) must never reach the customer channel. They are kept out of the
customer's index altogether ([decision D6](decisions.md)); v0.3.0 can move to per-user security trimming in
Azure AI Search.

## 4. Knowledge (RAG)

| Source | Content | Used by |
|---|---|---|
| SharePoint site "Contoso Bank Lending" | Short guides and the FAQ | Both agents from 0.2.0; shows SharePoint as knowledge |
| Azure AI Search index `loan-policy-public` | Blob container `knowledge-public`: the six public documents | Customer agent |
| Azure AI Search index `loan-policy-staff` | Blob container `knowledge`: all seven documents, including the internal credit manual | Staff agent |

Both indexes were built with the portal's **Import data → RAG** wizard (integrated vectorization):
- the data source is Azure Blob Storage (`stloandeskdev`), with native blob soft-delete tracking, so a
  document deleted from the container also leaves the index;
- a skillset splits each document into chunks and embeds them with `text-embedding-3-small`, deployed in
  Microsoft Foundry (`aif-loandesk-dev`); the same model embeds questions at query time;
- index fields: `chunk_id`, `parent_id`, `chunk`, `title` (the file name), `text_vector`;
- semantic ranker enabled; the indexer runs once, on demand.

The agents reach the indexes through **Foundry IQ** (agentic retrieval in Azure AI Search), because the
current Copilot Studio experience adds Azure AI Search as a tool, not as knowledge ([decision D8](decisions.md)):

```text
index loan-policy-public ─► knowledge source ks-loan-policy-public ─► knowledge base kb-loan-policy-public
                                                                         │ reasoning effort Minimal,
                                                                         │ output Extractive data
LoanDesk Customer Agent ─► tool "Foundry IQ Knowledge Retrieval MCP" ────┘ (query-key connection)
```

The staff side is the same with `loan-policy-staff`, `ks-loan-policy-staff` and `kb-loan-policy-staff`.

The front matter in each document (`doc_type`, `audience`, `effective_date`) is not mapped to index fields
yet. The index has no `metadata_storage_path`, so Copilot Studio citations show the file name without a
link; add the field if links are needed. Through the MCP tool, the readable file name is in each chunk's
`title` field, and the instructions make the agent end each answer with a `Source:` line.

Answer rules:
- Answer only from the sources; cite the document.
- If the sources do not answer the question, say so and offer a person.
- Never give a personal credit decision or promise approval.

## 5. Data model (Dataverse, from v0.2.0)

Solution publisher prefix: `ldk`.

Table **Loan Application** (`ldk_loanapplication`):

| Column | Type | Notes |
|---|---|---|
| Application number | Autonumber | `LDK-{SEQNUM:6}` |
| Business name | Text | Fictional |
| Business ID | Text | Fictional, used by the Credit Score API |
| Contact e-mail | Email | Fictional |
| Requested amount (THB) | Currency | |
| Term (months) | Whole number | |
| Purpose | Choice | Inventory, Payroll, Equipment, Other |
| Annual revenue (THB) | Currency | |
| Years in business | Whole number | |
| Eligibility result | Choice | Eligible, Not eligible, Needs review |
| Credit score | Whole number | From the mock API |
| AI summary | Multiline text | Written by a custom prompt; labelled as AI-generated |
| Status | Choice | Submitted, Under review, Approved, Rejected, Needs information |
| Decision reason | Multiline text | Required for Approved and Rejected |
| Decided by | Lookup (User) | The credit officer |
| Decided on | Date and time | |

## 6. Environment variables

| Name | Holds | Version |
|---|---|---|
| `ldk_SearchIndexPublic` | Customer index name (`loan-policy-public`) | 0.1.0 |
| `ldk_SearchIndexStaff` | Staff index name (`loan-policy-staff`) | 0.1.0 |
| `ldk_CreditApiBaseUrl` | Base URL of the Credit Score API | 0.2.0 |
| `ldk_McpServerUrl` | URL of the MCP server | 0.2.0 |
| `ldk_ApproverEmail` | Credit officer mailbox for approvals | 0.2.0 |

Secrets (API keys) are stored in connections or Azure Key Vault, never in environment-variable values that go
into source control.

## 7. Governance

These follow the shape of the Bank of Thailand's AI risk management guidelines for financial service
providers (September 2025), as a learning exercise:

| Principle | How LoanDesk does it |
|---|---|
| Human oversight, stronger for higher risk | Every application decision is a person's, in an approval step; the AI only pre-screens |
| Customers know they are talking to AI and can reach a person | The greeting says so; every topic can hand off to staff |
| Explainable outcomes | Answers cite documents; the AI summary is stored with the application and labelled |
| Reduce hallucination | RAG over approved documents only; out-of-scope questions are declined |
| Test before and after deployment | Test sets run on every change (Copilot Studio Kit, PromptDiff); Pipelines move only tested solutions |
| Monitoring | Application Insights and Copilot Studio analytics |
| Prevent data leakage | Internal documents stay out of the customer channel; no real data anywhere |

## 8. Environments

| Environment | Type | Purpose |
|---|---|---|
| `LoanDesk-Dev` | Sandbox with Dataverse, billed pay-as-you-go to Azure; macro region Asia Pacific | Build |
| `LoanDesk-Test` | Sandbox, same billing pattern | Deploy with Pipelines and run the test set (0.3.0) |

The pay-as-you-go billing plan uses two meters only: Dataverse (the first 1 GB of database and 1 GB of file
capacity per environment are included) and Copilot Studio (per Copilot Credit). Why not a Developer
environment: see [decision D5](decisions.md).

Azure resources live in one resource group, `rg-loandesk-dev`, with a USD 10 monthly budget alert:

| Resource | Name | Notes |
|---|---|---|
| Azure AI Search | `srch-loandesk-dev` | Free tier, Southeast Asia; two indexes |
| Storage account | `stloandeskdev` | Standard LRS, Hot; containers `knowledge` and `knowledge-public`; no anonymous access |
| Microsoft Foundry | `aif-loandesk-dev`, project `loandesk-dev` | Southeast Asia; deployment `text-embedding-3-small`, Global Standard, 10,000 tokens a minute |
| Power Platform billing plan | pay-as-you-go | Dataverse and Copilot Studio meters only |

Azure Functions follow in v0.2.0.
