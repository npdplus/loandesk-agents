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
