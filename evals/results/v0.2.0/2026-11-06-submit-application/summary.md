# Submit Application agent flow — 2026-11-06

End-to-end checks of the **Apply** topic on *LoanDesk Apply Agent* and the **Submit Application** agent flow,
from the Copilot Studio test pane to an approval in Power Automate and back to Dataverse. All data is
fictional (Microsoft's sample company names, `.example` addresses).

## Flow design

```text
When an agent calls the flow        inputs: BusinessName, BusinessID, ContactEmail (text); RequestedAmount,
                                     TermMonths, AnnualRevenue, YearsInBusiness (number); Purpose (text)
Add a new row (Dataverse)           ldk_loanapplication, status Submitted (852190000); Purpose text mapped to
                                     its choice value with an if(...) expression
├─ Respond to the agent             ApplicationNumber, Status "Submitted", Message   (run after: succeeded)
│  Get approver email (List rows)   Environment Variable Definitions, schemaname eq 'ldk_ApproverEmail',
│                                     expanded to its current value
│  Start and wait for an approval   Approve/Reject - First to respond; assigned to the approver e-mail
│  Condition Outcome = Approve
│    ├─ Approved (Update a row)     status Approved (852190002); decision reason, decided by, decided on
│    └─ Rejected (Update a row)     status Rejected (852190003); same three columns
└─ Respond to the agent - error     ApplicationNumber "-", Status "Error", Message with the Lending Centre
                                     contact                                (run after: failed, timed out)
```

The agent gets its answer right after the row is created; the approval continues in the background. An agent
waits only a short time for a flow, so it must never wait for a person.

## Runs

| Run | Application | Result in the agent | Approval | Row after the run | Run status |
|---|---|---|---|---|---|
| 1 | LDK-000003, Contoso Coffee | Number given | None: the approval step failed (see below) | Submitted (left as is) | Failed |
| 2 | LDK-000004, Contoso Coffee, THB 500,000, 12 months | "Your application number is LDK-000004" | Approved, "A01: approved as requested" | Approved; reason, decided by and decided on filled | Succeeded |
| 3 | LDK-000005, Tailspin Toys, THB 3,500,000, 36 months | "Your application number is LDK-000005" | Rejected, "D03: DSCR below guidance" | Rejected; reason, decided by and decided on filled | Succeeded |

## Problems found and fixed

1. **Environment variable not found at run time.** Agent flows do not list environment variables in dynamic
   content. A typed `parameters('Approver email (ldk_ApproverEmail)')` saved and published, but run 1 failed
   with "The workflow parameter … is not found". Fixed by reading the variable from Dataverse: *List rows* on
   *Environment Variable Definitions*, expanded to its value, and
   `coalesce(<current value>, <default value>)` in *Assigned to*.
2. **Two "Respond to the agent" actions must match.** Publishing failed with "The schema definitions for
   actions with same status code must match" until both actions had the same outputs with the same names,
   types **and descriptions**.
3. **Agent flows join the solution on publish.** The draft flow could not be added with *Add existing*; after
   the first publish it appeared in solution LoanDesk by itself.
4. **A topic left unsaved is lost.** The first Apply topic was never saved before *New Agent flow* opened the
   flow designer; the topic was rebuilt. Save a topic before any step that leaves the page.
5. **Typed variable names are text.** In *Add a new row*, typed `AnnualRevenue` etc. failed as "Enter a valid
   number"; each value must be a dynamic-content token.

## Open items

- If the approval step fails, nothing updates the row (LDK-000003 stays Submitted). Add a branch that sets
  *Needs information* when the approval fails or times out.
- The approval *Details* lose their line breaks (the approval renders Markdown); add blank lines.
- *Decision reason* was created as Rich text; plain text would fit the approval comment better.

## Step 7: notification e-mail (same day)

A parallel branch after *Respond to the agent*: **Get notify email** (*List rows* on environment variable
`ldk_NotifyEmail`, same pattern as the approver) → **Send an email (V2)** (Office 365 Outlook). The approval
branch does not wait for it.

| Run | Application | E-mail | Result |
|---|---|---|---|
| 4 | LDK-000006, Wingtip Toys | Sent, but to the approver address | Bounced, 550 5.1.10 RecipientNotFound: the approver account has no mailbox |
| 5 | LDK-000007, Wingtip Toys | "New loan application LDK-000007" to the notification mailbox | Delivered; all fields filled |

Cause of run 4: the *Get notify email* action was copied from *Get approver email* and its filter still read
`ldk_ApproverEmail`. When copying an action, check every value that names the thing it reads.

Connector choice: the *Mail* connector's *Send an email notification (V3)* sends through Azure Communication
Services and SendGrid, which may process data outside the environment's region, and needs its terms
accepted. *Office 365 Outlook* keeps the message in Exchange Online and sends from a real mailbox, as a bank
would require; it was chosen. The Outlook connection signs in as the mailbox owner, not as the maker.
