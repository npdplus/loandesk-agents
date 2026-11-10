---
title: LoanDesk Approvals — Staff Quick Guide
bank: Contoso Bank (fictional)
doc_type: guide
audience: internal
effective_date: 2026-11-10
---

# LoanDesk Approvals — Staff Quick Guide

**Contoso Bank (fictional). INTERNAL — staff only.** This document is part of a demo. Contoso Bank, its
products and procedures are not real. It is kept on the SharePoint site *Contoso Bank Lending*, not in the
search indexes.

## 1. Where approval requests arrive

Every application submitted through the LoanDesk assistant sends one approval request to the credit officer
on duty. It appears in Power Automate → Approvals, in Teams (Approvals app) and by e-mail, with the title
**Loan application LDK-nnnnnn – business name**. The details list the amount, term, purpose, annual revenue,
years in business, business ID and the mock credit score (staff only).

## 2. Respond within 7 days

- An approval request **expires after 7 days**. The application status then changes to **Needs information**
  with the reason "Approval not completed (failed or timed out)".
- An expired request can still show in your list. Answering it has **no effect**: check the status of the
  application in LoanDesk before you act.
- To restart an expired application, ask the Lending Centre team lead to set the status back to *Submitted*
  and send a new approval request.

## 3. How to write the comment

Start the comment with a **reason code** from the Credit Officer Manual (section 5), then one short sentence:

| Example | Use |
|---|---|
| `A01: approved as requested` | Approve |
| `A02: approved for THB 800,000 to bring DSCR to guidance` | Approve a lower amount |
| `D04: bank statements do not match the revenue stated` | Decline |
| `N01: audited financial statements for 2025 missing` | More information needed |

The comment is stored with the application as the decision reason. Write it so that a colleague who reviews
the application later understands the decision without asking you.

## 4. When the credit score says "not available"

The Credit Score service has no file for the business. Decide from the documents and the other rules, and say
in the comment that no score was available. Do not decline only because there is no score.

## 5. What you must not do

- Do not forward an approval request or its details to the customer.
- Do not approve your own application or one from a business you are connected to; ask the team lead to
  reassign it.
- Do not approve or decline based only on the AI summary.
