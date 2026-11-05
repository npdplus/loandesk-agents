# Decisions

One entry per decision that shapes the design. Newest last.

## D1 — The AI never decides a loan (2026-11-02)

The agents answer, pre-screen and summarise. Approval and rejection are always a credit officer's, in an
approval step, with a recorded reason. Reason: human oversight for high-risk decisions, as banking AI
guidance expects.

## D2 — Fictional bank and data only (2026-11-02)

The bank is Contoso Bank, Microsoft's fictional company. No real bank name, customer, person or document is
used anywhere, including test sets and screenshots.

## D3 — Two agents per audience in v0.1.0 (2026-11-02)

A customer agent and a staff agent, each with its own knowledge, rather than one agent that filters by user.
Reason: the simplest way to keep internal documents out of the customer channel before per-user security
trimming is added.

## D4 — Low-cost Azure (2026-11-02)

Azure AI Search Free tier, pay-as-you-go models in Microsoft Foundry, Azure Functions on the consumption plan,
and a USD 10 budget alert on `rg-loandesk-dev`. Resources that are not needed between sessions are deleted.

## D5 — A pay-as-you-go Sandbox, not a Developer environment (2026-11-02)

Microsoft is retiring unmanaged Developer environments: none can be created from 15 November 2026, existing
ones are suspended from 15 December 2026 and deleted from 15 January 2027. A Copilot Studio trial environment
lasts 30 days, and a managed Developer environment needs premium licences.

`LoanDesk-Dev` is therefore a Sandbox with Dataverse, linked to a pay-as-you-go billing plan in
`rg-loandesk-dev`, so its cost counts against the same budget. The plan turns on only the Dataverse and
Copilot Studio meters; Power Apps and Power Automate stay off (no apps, and premium flow runs would be billed
per run). The system chose the region inside the Asia Pacific geography (Japan), and the billing plan matches
it. Data residency does not matter here because all data is fictional.

## D6 — Two vector indexes, one per audience (2026-11-02)

Copilot Studio connects an agent to **one** Azure AI Search vector index, expects integrated vectorization,
and its documentation does not describe filtering that index per agent. One index with an `audience` filter
could therefore not guarantee that the customer agent never retrieves the internal credit manual.

So there are two indexes: `loan-policy-public` (the six public documents) for the customer agent and
`loan-policy-staff` (all seven) for the staff agent. The public documents are stored twice, which is
acceptable at this size. The Free tier allows three indexes.

Related choices, to revisit in v0.3.0:
- **Embedding model:** `text-embedding-3-small` on a Global Standard deployment with a 10,000 tokens-a-minute
  cap. Global Standard may process data outside the resource's geography; a real bank would choose a
  regional (Standard) or Data Zone deployment.
- **Authentication:** API keys between Search, Storage and Foundry for now; managed identities later.
- **Semantic ranker:** enabled. Check that the service uses the free semantic ranker plan.

Update 2026-11-05: the portal's *Premium features* page shows the semantic ranker and knowledge retrieval
both on the **Free** plan (USD 0 a month); the Standard plans cannot be selected on the Free tier.

## D7 — A Copilot Studio trial licence for the maker (2026-11-03)

Saving an agent needs a Copilot Studio user licence, even in a pay-as-you-go environment. What was tried:

- The tenant setting *Copilot Studio pay-as-you-go users* set to an Entra group of makers: needed, not enough.
- The USD 0 *Microsoft Copilot Studio User License*: needs the paid *Microsoft Copilot Studio* capacity pack
  as a prerequisite.
- The admin-centre *Microsoft Copilot Studio (Trial)*: **converts to a paid one-year subscription** when the
  trial ends. Not ordered.

Chosen: the self-service individual trial (sign-up from Copilot Studio). It can build and test agents but
cannot **publish** them; it lasts 30 days and can be extended once by 30 days. So v0.1.0 tests agents in the
Preview pane, and channels move to a later version. The Preview pane shows the Copilot Credits each
conversation uses; the tests on 2026-11-05 showed 0.

## D8 — Azure AI Search through a Foundry IQ knowledge base (2026-11-05)

The current Copilot Studio experience has no *Azure AI Search* option under **Knowledge**. Search is added as
a **tool**: the Microsoft *Azure - Foundry IQ* MCP server, which calls a **knowledge base** in Azure AI Search
(agentic retrieval). The chain is index → knowledge source → knowledge base → MCP tool → agent.

| Object | Customer agent | Staff agent |
|---|---|---|
| Knowledge source (type *Search index*) | `ks-loan-policy-public` → `loan-policy-public` | `ks-loan-policy-staff` → `loan-policy-staff` |
| Knowledge base | `kb-loan-policy-public` | `kb-loan-policy-staff` |

Settings, chosen to keep cost at zero and the answer under the agent's control:

- **Reasoning effort: Minimal.** No LLM query planning, so no Foundry model is needed and nothing is billed
  outside the Search free allowance (50 million agentic retrieval tokens a month on the Free plan).
- **Output mode: Extractive data.** The knowledge base returns chunks; the agent writes the answer.
- Source data fields and search fields: `chunk`, `title`; the index's semantic configuration.
- **Connection: a query key**, not an admin key. A query key can retrieve but cannot change or delete
  anything. Side effect: the tool set-up cannot list knowledge bases, so the name is typed in.

Citations: the tool returns each chunk with a `Title` of the chunk ID and a `URL` of `mcp://searchindex/...`,
which Copilot Studio cannot show as a readable link. The file name is in the chunk's `title` field, so the
instructions tell the agent to end each answer with a `Source:` line listing those file names.

The same MCP tool also gives early practice with *Configure MCP tools*, planned in full for v0.2.0.

## D9 — Model and agent names (2026-11-03)

- **Model:** Claude Sonnet 5.5. Reasoning models are billed by Copilot Studio as premium, per 1,000 tokens,
  so they are avoided in this demo.
- **Names:** the agent name field holds about 30 characters, so the agents are *LoanDesk Customer Agent* and
  *LoanDesk Staff Agent* (planned as *Contoso Policy Agent (customer/staff)*).

## D10 — Work IQ capability components left on the agents (2026-11-05; removal due before v0.2.0)

A new agent starts with the *Work IQ* tool, which grounds answers in the signed-in user's Microsoft 365 mail,
calendar, files, people, sites and Teams. It was removed from both agents (the staff agent before its first
save). The solution export still holds six components per agent of kind `IQCapability`, each with
`access: Write`, while each agent's configuration says `WorkIqAddedByDefault: false` and lists only the
Foundry IQ tool.

The agents do not need Microsoft 365 data, and least privilege says they should not have it. Next steps:

- Test in Preview whether the customer agent can read the maker's calendar or mail. **Done 2026-11-05:**
  "What is on my calendar today?" got "I can only help with the SME Working Capital Loan, so I can't see your
  calendar", and the debug view showed no tool call. No sign the components are active.
- That does not prove they are inert: the instructions alone could explain the refusal. Before v0.2.0
  publishes the agents, remove the components and export again.
