# Customer agent checks — 2026-11-05

Manual checks of the knowledge base `kb-loan-policy-public` (Azure portal chat pane) and of the
*LoanDesk Customer Agent* (Copilot Studio Preview pane, debug mode on). Set-up:
[decision D8](../../../../docs/decisions.md).

## Knowledge base (Azure portal)

Reasoning effort Minimal, output mode Extractive data.

| # | Query | Expected | Result | Pass |
|---|---|---|---|---|
| K1 | minimum annual revenue | THB 1,200,000 with sources | Chunks from `eligibility-policy.md` (rule E3), `product-sheet.md`, `faq.md`, all from `ks-loan-policy-public` | Yes |
| K2 | DSCR | Nothing from the internal credit manual | "I don't have any answer for you." | Yes |

## Customer agent (Copilot Studio Preview)

Tool: *Foundry IQ Knowledge Retrieval MCP* (`knowledge_base_retrieve`) with a query-key connection.

| # | Question | Expected | Result | Pass |
|---|---|---|---|---|
| C1 | What is the minimum annual revenue to apply? | THB 1,200,000, cites a document | THB 1,200,000 (rule E3). No readable citation; offered a pre-check the agent cannot do yet | Partly |
| C2 | What DSCR does the bank require for approval? | Declines; no internal content; offers a person | Said approval thresholds are internal; listed the public rules; offered the Lending Centre | Yes |
| C3 | C1 again, after the instruction changes below | THB 1,200,000 and a `Source:` line; no pre-check offer | THB 1,200,000; "Source: eligibility-policy.md, faq.md, product-sheet.md"; no pre-check offer | Yes |

All three conversations showed 0 Copilot Credits in the Preview pane.

## Changes made after C1 and C2

Two instruction lines:

- Answer only from what `knowledge_base_retrieve` returns, and end every answer with a `Source:` line listing
  the file names from the `title` field.
- Offer only what the agent can do now (answer, connect to a person); no pre-check or application yet.

## Lessons

- The tool output gives each chunk a `Title` of its chunk ID and a `URL` of `mcp://searchindex/...`, so the
  built-in citations cannot show a readable source. The `title` field inside each chunk has the file name.
- For C2 the tool still returned eight chunks, all public. The portal chat (K2) returned none. Either way
  the customer index holds no internal content, and the instructions keep the agent from guessing.
- The tool output reports `agenticReasoningTokens` (3,703 for C2, 7,404 for C3). These are Azure AI Search
  tokens inside the free monthly allowance, not LLM charges.
- A query key is enough for retrieval. It cannot list knowledge bases, so the tool set-up shows "Could not
  load options" and the name is typed in.
