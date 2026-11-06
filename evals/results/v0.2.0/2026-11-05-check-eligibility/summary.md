# Check eligibility topic — 2026-11-05

Manual checks of the **Check eligibility** topic in *LoanDesk Apply Agent* (standard harness, decision D11),
in the Copilot Studio test pane. Each case started with *New test session* and "Can my business apply?".

## Topic design

```text
Trigger: the agent chooses (description of the topic)
Ask with adaptive card  (docs/cards/eligibility-card.json)
  outputs: yearsInBusiness, annualRevenue, requestedAmount (number); termMonths (string)
Condition E2: yearsInBusiness < 2                          → message E2
  else Condition E3: annualRevenue < 1,200,000            → message E3
    else Condition R1: amount < 100,000 OR > 5,000,000    → message R1
      else Condition R2: amount > Topic.annualRevenue * 0.3 (formula)
                                                          → message R2 with
                                                            Text(Min(Topic.annualRevenue * 0.3, 5000000), "#,##0")
        else                                              → "Eligible to apply…"
Message (all paths): "This pre-check is not a loan decision. A credit officer reviews every application."
```

R3 (term) always passes: the card offers only the allowed terms.

## Cases

| # | Years | Revenue | Amount | Term | Expected | Result | Pass |
|---|---|---|---|---|---|---|---|
| T1 | 2 | 1,500,000 | 600,000 | 24 | R2, up to THB 450,000 | "Not eligible as requested. Rule R2 … up to THB 450,000" | Yes |
| T2 | 3 | 2,000,000 | 500,000 | 12 | Eligible | "Eligible to apply. Your answers meet rules E2, E3, R1, R2 and R3." | Yes |

Both cases match the worked examples in `knowledge/eligibility-policy.md`, and both end with the pre-check
disclaimer.

## Lessons

- **A formula must show the `fx` icon.** The first build used one *Set variable value* with a long Power Fx
  `If(...)`. The value was stored as plain text at first and the message showed nothing; even after it showed
  `fx`, the result stayed empty and the cause was not found. The topic was rebuilt with one Condition node per
  rule, which is easier to read and to debug, and formulas only where needed.
- **"New condition" inside a Condition node adds an AND/OR clause, not a branch.** Rules are chained through
  each node's *All other conditions* branch.
- **Check the operator after building.** R2 was first saved as "is less than", which would have reversed the
  results; it was caught in review before testing.

## Explain my result: custom prompt (2026-11-06)

The topic now explains its result in plain words with a **custom prompt**, after the rules have decided it.

```text
Set variable eligibilityResult = ""          (before the branches, so every branch can see it)
  each branch: Message (rule text) → Set variable eligibilityResult (same text; R2 as a formula)
Prompt "Explain eligibility result"          model GPT-4.1 mini, output Text
  input EligibilityResult = Topic.eligibilityResult; output → Topic.explanation (record)
Message "In plain words (AI-generated): " + Topic.explanation.text
Message "This pre-check is not a loan decision. A credit officer reviews every application."
```

Prompt instructions: explain the pre-check result in 2 to 4 sentences; say what the customer could change
using only facts in the result; add no rules, numbers, rates or fees; never suggest approval.

| # | Case | Prompt output | Pass |
|---|---|---|---|
| T3 | T1 again (R2, up to THB 450,000) | Explains the 30 % limit, gives THB 450,000 as the maximum, suggests lowering the request, says a credit officer decides; no new numbers | Yes |

The prompt test in the prompt editor used 0.2 Copilot Credits.

Lessons:

- **The rules decide; the model only explains.** The prompt never sees the four answers, only the result
  text, so it cannot recompute or override the decision (decision D1).
- **Declare a variable before the branches.** A variable created in one Condition branch was not offered in
  the sibling branches. Setting it to `""` before the first Condition made it available everywhere.
- **Prompt input values need the `{x}` chip** (typed `eligibilityResult` saved as text, and the topic then
  failed to save with "An unexpected error occurred while saving the dialog").
- The prompt was saved twice, so the solution holds an unused *Explain eligibility result* next to the used
  *Explain eligibility result 1*. Remove the unused one before the next export.
