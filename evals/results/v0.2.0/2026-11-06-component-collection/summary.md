# Component collection — 2026-11-06

**LoanDesk shared components**, created from *LoanDesk Apply Agent* (*Settings → Component collections →
Create*), in solution LoanDesk, with one topic: **Talk to a person** (the Lending Centre contact, from
`faq.md` and `privacy-and-ai-notice.md`).

| # | Check | Result | Pass |
|---|---|---|---|
| CC1 | "I want to talk to a person" before the collection | Talk to a person topic; Lending Centre e-mail and hours | Yes |
| CC2 | Collection created; *Installed on* | LoanDesk Apply Agent | Yes |
| CC3 | CC1 again after the topic moved into the collection | Same topic and answer | Yes |

Notes:

- Component collections work only with **standard-harness** agents (Microsoft Learn, *Create and share
  reusable component collections*). The customer and staff agents use the new harness, so the collection has
  one agent for now; v0.3.0's Front Desk agent (standard harness) is the second consumer.
- Creating a collection **moves** the selected components into it; the source agent keeps them through the
  installed collection.
- Knowledge files were left out on purpose: adding an uploaded file to a collection removes it from the
  source agent, which would break the Rates topic.
- The environment also lists a Microsoft collection, *AppCopilot_ComponentCollection_V1*, under *Available*;
  it is not used.
