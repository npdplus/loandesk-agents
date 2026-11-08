# Foundry project and model — v0.3.0 step 1

Date: 2026-11-08.

## Resource

- **Microsoft Foundry** resource `aif-loandesk-dev-03` in `rg-loandesk-dev`, Southeast Asia, with the default
  project `proj-loandesk` (new Foundry portal). Basic setup: no Key Vault, Application Insights, Cosmos DB,
  AI Search or storage account of our own; Foundry keeps agent threads and files itself. Inbound access from
  all networks, no outbound network isolation, system-assigned identity, Microsoft-managed keys, tagged
  `application=loandesk`, `environment=dev`. (The names `aif-loandesk-dev` and `-01`/`-02` were taken.)
- **Deployment** `gpt-4.1-mini` (2025-04-14), **Global Standard**, **10,000 tokens per minute** (lowered from
  the default to cap spend), default guardrails. Global Standard may process prompts outside the resource's
  geography; data at rest stays in it. Acceptable here because every input is fictional.
- The default deployment settings would have used the full quota; *Custom settings* was used instead.

## Checks

| # | Check | Result |
|---|---|---|
| F1 | Playground: "Reply with one short sentence: what is an SME working capital loan?" | Pass: one correct sentence, about 1 s, 59 tokens |
| F2 | Web search tool removed from the playground before the test | Done (Grounding with Bing is billed separately and sends data outside Azure) |
| F3 | "You don't have permission to create agents in this project" | Fixed: the creator had only **Owner** inherited from the subscription (control plane). Added **Foundry User** on the resource for the maker; the warning was gone after a refresh |

Lesson: Owner on the subscription does not give the data-plane rights a Foundry project needs. The portal
said it would grant Foundry User automatically, but it did not; check *View my access* after creating a
Foundry resource.
