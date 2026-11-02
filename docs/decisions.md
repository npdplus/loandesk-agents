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
