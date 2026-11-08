# Step 0 spikes — v0.3.0

Date: 2026-11-08.

## Foundry model

- Prompts with "bring your own model" need a **chat completions** deployment and do not support the GPT-5
  family. Foundry agents can use either.
- `gpt-4.1-mini` (2025-04-14) is deprecated but retires on **2027-04-14** in Azure public cloud, long after
  this project. Chosen for both the prompt (step 2) and the Document Agent (step 3), as one Global Standard
  deployment.
- Region: the region tables available online did not confirm Southeast Asia for this model. Checked in the
  portal when deploying in step 1; if it is missing there, the nearest region with Global Standard is used.

## Copilot connector

- The tenant has **Microsoft 365 Business Basic** (active, 1 licence; Business Standard is disabled) and
  Microsoft Entra ID Free. Business Basic includes Microsoft Search.
- Microsoft 365 admin center → **Copilot → Connectors** is available, with a Gallery and existing
  connections (prebuilt third-party connections listed as Ready). A Microsoft 365 Copilot licence is not
  required for Copilot connectors as Copilot Studio knowledge; it only improves search results.
- Verdict: a Copilot connector can be set up. The connector and its source are chosen in step 5 (a public,
  fictional source only).
