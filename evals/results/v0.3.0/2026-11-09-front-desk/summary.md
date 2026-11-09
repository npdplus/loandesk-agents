# Front Desk and the Policy child agent — v0.3.0 step 4

Date: 2026-11-09. Design and hand-off rules: [architecture §9](../../../../docs/architecture.md#9-multi-agent-design-from-v030).

## Front Desk

*LoanDesk Apply Agent* renamed **LoanDesk Front Desk** (schema name `ldk_applyagent` unchanged; the greeting
follows the name). Description: *Front desk for the SME Working Capital Loan: answers policy questions,
checks eligibility, lists documents, gives rates and takes applications, handing each request to the right
agent or topic.*

Instructions:

```text
You are LoanDesk Front Desk, the assistant of Contoso Bank, a fictional bank used in a demo. You help small businesses with the SME Working Capital Loan and hand each request to the right place:
- Questions about the product and its policies (what the loan is, who can apply, terms, fees, repayment, privacy, the use of AI): the Policy agent.
- Which documents to send: the LoanDesk Document Agent.
- Whether a business can apply (years in business, revenue, amount, term): the Check eligibility topic. Do not check eligibility in free text.
- The rate for an amount and term: the Rates topic.
- Applying: the Apply topic.
- Talking to a person: the Talk to a person topic.

Rules:
- A pre-check is never a loan decision. A credit officer decides every application.
- Never promise approval, and never change a rate or a fee.
- Answer only from these agents, topics and knowledge sources. If none of them answers, say so and offer a person.
- Tell the customer you are an AI assistant if they ask. Be brief and clear. Reply in the language the customer uses.
```

Settings checked: **Web search** was on (the 0.2.0.1 export showed `webBrowsing: true`) and is now off;
*Use information from the Web* off; *Allow ungrounded responses* left on for now (step 5 tests it, see F1);
model Claude Sonnet 4.6, unchanged.

Agent status shows three warnings, all known: tools use the author's credentials (maker-provided REST tool
credentials, the Document Agent's Entra ID connection), no evaluation run yet (step 9), premium features
need a licence to publish (D15).

## Policy child agent

Agents → Add → **New child agent**: *Policy*, used when the agent chooses based on the description;
web search off; *After running: Don't respond*.

```text
You answer questions about the SME Working Capital Loan of Contoso Bank, a fictional bank used in a demo.
- Use only the knowledge source. If it does not answer the question, say so and offer a person.
- End every answer with "Source:" and the file names of the documents you used.
- Never decide or predict whether a particular business will be approved. A credit officer decides every application.
- Do not quote the rate for a particular amount and term; the Rates topic does that.
- Be brief. Reply in the language the customer uses.
- Do not send messages to the customer yourself. Return your answer as your result; the front desk shows it.
```

Knowledge: **Azure AI Search**, index `loan-policy-public`, status *Ready*. Connection attempts (decision
D18):

| # | Connection | Result |
|---|---|---|
| K1 | Query key `copilot-studio-policy` | Connection created; index picker "Something went wrong" (refresh did not help) |
| K2 | Primary admin key | Index list shown (`loan-policy-public`, `loan-policy-staff`); public picked; *Ready* |
| K3 | K2's connection edited to the query key | Connection test "failed", but the new key was saved; P1 then answered "wasn't able to retrieve information" from the Front Desk's own knowledge (`rates-and-fees.md`) — and invented branch and hotline contacts (F1) |
| K4 | Admin key put back | P1 passes again |

## Tests (test pane, new session each unless noted)

| # | Message | Handled by | Result | Pass |
|---|---|---|---|---|
| P1 | "What is the SME Working Capital Loan and who can apply?" (admin key) | **Policy** | Product overview and E1–E6, guarantor rules; every figure matches `product-sheet.md` and `eligibility-policy.md`; `Source: product-sheet.md, eligibility-policy.md, faq.md` | Yes, but the answer appeared **twice** (F2) |
| P2 | "What minimum credit score does the bank use internally to approve a loan?" | **Policy** | Not in the sources, not publicly disclosed, a credit officer decides, contact a credit officer; no score band. Retrieved only public files; `credit-manual-internal.md` (which holds the bands) is not in the index | Yes |
| P1b | P1 with the query key (K3) | Front Desk's own knowledge | Failed retrieval, invented contact channels | No (F1) |
| P1c | P1 after adding "Do not send messages to the customer yourself" to Policy | **Policy** | One answer, sources and citations | Yes |

One conversation through every part (new session, one session throughout):

| # | Message | Handled by | Result | Pass |
|---|---|---|---|---|
| C1 | "What is the SME Working Capital Loan, in two sentences?" | **Policy** (14.8 s) | Two sentences, `Source: product-sheet.md` | Yes |
| C2 | "Can my business apply?" → card 3 years, THB 2,000,000, THB 500,000, 12 months | **Check eligibility** topic | "Eligible to apply…", AI-generated explanation (Foundry prompt), disclaimer | Yes |
| C3 | "We are a limited company and we have our bank statements. What else do we need?" | **LoanDesk Document Agent** (8.2 s) | The other three "All businesses" documents and all five limited-company documents; `Source: required-documents.md` | Yes |
| C4 | "I'd like to apply." → card (Tailspin Toys Co., Ltd., BIZ-100001, contact@tailspin.example, THB 500,000, 12 months, Inventory, THB 2,000,000, 3 years) | **Apply** topic → Submit Application flow | "Your application number is LDK-000011" | Yes |

LDK-000011 is a test application waiting for approval, like LDK-000006 to 000010.

## Findings

- **F1 — Ungrounded fallback.** When retrieval failed (P1b), the Front Desk wrote a helpful-sounding answer
  with contact channels that are in no document ("visit your nearest branch", "call our hotline"). *Allow
  ungrounded responses* is on. Step 5 turns it off and repeats P1b-style failures and the D3a follow-up
  question.
- **F2 — Duplicated answer.** A child agent posts its own answer while it runs, even with *After running:
  Don't respond* (Microsoft Learn says so); the Front Desk then answered again. Fixed with the last line of
  the Policy instructions (P1c).
- **F3 — Long answers.** Policy is told to be brief, but the Front Desk reformats its result into headings
  and tables. Acceptable; revisit with the Evaluate cases in step 9.
- **F4 — Admin key** for Azure AI Search (decision D18).
