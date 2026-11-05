# Staff agent checks — 2026-11-05

Manual checks of the knowledge base `kb-loan-policy-staff` (Azure portal chat pane) and of the
*LoanDesk Staff Agent* (Copilot Studio Preview pane, debug mode on). Same settings as the customer side
([decision D8](../../../../docs/decisions.md)); the tool reuses the query-key connection.

## Knowledge base (Azure portal)

| # | Query | Expected | Result | Pass |
|---|---|---|---|---|
| K3 | DSCR | The credit manual | Two chunks of `credit-manual-internal.md` from `ks-loan-policy-staff`: assessment steps, decision guide, four-eyes rule, reason codes | Yes |

K2 (customer side, same query, no answer) and K3 together show the audience split at the knowledge-base
level.

## Staff agent (Copilot Studio Preview)

| # | Question | Expected | Result | Pass |
|---|---|---|---|---|
| S1 | What DSCR does the bank require for approval? | DSCR bands from the manual; no decision; a reminder not to tell customers; `Source:` line | Decision guide table (1.25 at 700+, 1.50 at 600–699), DSCR formula, four-eyes rule, code D03; "You make the decision"; reminder; "Source: credit-manual-internal.md" | Yes |

0 Copilot Credits shown. The tool output reported 9,074 agentic retrieval tokens (Search free allowance).

## Set-up notes

- A new agent starts with the model *Claude Opus 5.5*, the tool *Work IQ* (the user's Microsoft 365 mail,
  calendar and files) and the knowledge *Search all websites*. All three were changed: model Claude Sonnet
  5.5, Work IQ and web search removed.
- The question S1 against the customer agent is C2 in
  [the customer results](../2026-11-05-customer-agent-preview/summary.md): declined, no internal content.
