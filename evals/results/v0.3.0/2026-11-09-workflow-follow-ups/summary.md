# Workflow follow-ups from v0.2.0 — v0.3.0 step 6

Date: 2026-11-09. Agent flow **Submit Application** (solution LoanDesk), edited in Power Apps → Solutions →
LoanDesk → Cloud flows. Design before the change: `evals/results/v0.2.0/2026-11-06-submit-application/`.

## Changes

```text
Start and wait for an approval      Details as a Markdown list; timeout P7D (PT3M while testing)
├─ Condition Outcome = Approve      run after: approval succeeded           (unchanged)
│    ├─ Approved (Update a row)
│    └─ Rejected (Update a row)
└─ Needs information (Update a row) run after: approval failed, skipped or timed out          (new)
                                     status Needs information (852190004); decision reason
                                     "Approval not completed (failed or timed out). A credit officer
                                     must review this application."; decided by and on left empty
```

1. **Line breaks.** The approval renders *Details* as Markdown, so single line breaks were lost. Each line
   now starts with `- `, and a blank line separates the closing sentence.
2. **Needs information.** A parallel branch after the approval, so the Condition still runs only when the
   approval succeeds. (Inserting the action between the approval and the Condition would have made the
   Condition depend on it and be skipped after every normal decision; the branch was moved to be parallel
   before testing.)
3. **Timeout.** The approval waits at most **P7D** (7 days; the product promises a decision within 5 business
   days). Before, it had no timeout and waited up to the 30-day platform limit.
4. **Credit score expression (bug found by the new branch).** The *Details* line
   `if(empty(triggerBody()?['number_4']), …)` failed the approval whenever a score was present, because
   `empty()` does not accept an integer (R4a fix of 2026-11-07). Now
   `if(equals(triggerBody()?['number_4'], null), 'not available', string(triggerBody()?['number_4']))`.

Edits in the newer designer are saved as a **draft** ("We saved your draft flow. You can test and run it
after you publish"); runs keep using the published version until **Publish**. The classic designer's Save
published at once.

## Runs

| # | Application | Approval | Flow run | Row after the run | Pass |
|---|---|---|---|---|---|
| W0 | LDK-000011 (10:42, step 4, BIZ-100001, score 881) | None: `empty()` on an integer | Failed in 2 s, before the new branch existed | Submitted (stuck) | — (found the bug) |
| W1 | LDK-000012 (BIZ-100009, score 659) | None: same expression error | Failed in 1 s; **Needs information** succeeded | Needs information, with the reason | Yes (failed path) |
| W2 | LDK-000013 (BIZ-100009), after the expression fix, timeout PT3M | Arrived; Details as a list, score 659; not answered | *ActionTimedOut* after 3 min 1 s; **Needs information** succeeded; Condition skipped | Needs information | Yes (timed-out path, line breaks) |
| W3 | LDK-000014 (BIZ-100002, score 414), timeout change still a draft | Arrived; Details as a list, score 414 | Timed out after 3 min on the published PT3M version; Needs information | Needs information | Yes (again) |
| W4 | LDK-000015 (BIZ-100002), P7D published | Approved, "A01: approved as requested" | Condition → Approved; Needs information skipped | Approved; decided by, decided on 2:13 PM, reason | Yes (normal path) |

A handled timeout still shows the run as **Failed**, because the approval action failed. That is useful: the
run history and the error trend show every application that nobody decided.

## Notes

- A timed-out approval stays in the approver's *Received* list (LDK-000013, 000014). Answering it later has
  no effect: the flow has ended. The row in Dataverse is the record.
- Left as test data: LDK-000006 to 000010 still wait for an answer (one run from 2026-11-07 is still
  *Running*, with no timeout); LDK-000011 stays *Submitted*. The approver can reject the open requests at any
  time; LDK-000011 can be set to *Needs information* by hand.
- Each test application costs an agent turn, an agent flow run and an approval; the five runs here are
  within the budget checked in step 2.
