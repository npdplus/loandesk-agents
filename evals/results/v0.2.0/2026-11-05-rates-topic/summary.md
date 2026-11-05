# Rates topic — 2026-11-05

Manual check of the **Rates** topic in *LoanDesk Apply Agent* (standard harness), in the Copilot Studio test
pane, with *New test session*.

## Topic design

- Trigger: the agent chooses, from the description "Answers questions about interest rates and fees for the
  SME Working Capital Loan: the rate for an amount and term, the front-end fee, early repayment and late
  payment."
- **Create generative answers** node (the *generative answers node*):
  - Input: the system variable `Activity.Text` (the customer's message)
  - Knowledge sources: **Search only selected sources** on, with one file, `rates-and-fees.md`, uploaded to
    the agent's knowledge (*topic-level knowledge*)
  - Web search off; *Allow the AI to use its own general knowledge* off

## Cases

| # | Question | Expected | Result | Pass |
|---|---|---|---|---|
| R-1 | What is the interest rate for THB 4,000,000 over 36 months? | 7.00 % a year | No answer: "There is no information about 'Activity.Text'"; the input held the words, not the variable | No |
| R-2 | Same, after the input was set to the variable | 7.00 % a year | 7.00 % for THB 3,000,001–5,000,000 over 36 months, fixed, reducing balance; 1 reference, `rates-and-fees.md` | Yes |

## Lesson

In the standard harness, a field that should hold a value from a variable must show the `{x}` chip (or `fx`
for a formula). Typed text, even the name of a variable, is a literal string. The same cause hid the first
eligibility result (see `../2026-11-05-check-eligibility/`).
