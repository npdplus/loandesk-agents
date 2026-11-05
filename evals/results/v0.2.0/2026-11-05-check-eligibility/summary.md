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
