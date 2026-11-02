# Search explorer checks — 2026-11-02

Manual queries in the Azure portal's Search explorer against `srch-loandesk-dev`, right after the first
indexer runs. Hybrid query (text and vector) with semantic ranker. Scores are as shown in the portal.

## Indexers

| Indexer | Status | Documents | Chunks in index |
|---|---|---|---|
| `loan-policy-public-indexer` | Success, 0 errors, 0 warnings | 6/6 | 9 |
| `loan-policy-staff-indexer` | Success, 0 errors, 0 warnings | 7/7 | 11 |

## Queries

| # | Index | Query | Expected | Result | Pass |
|---|---|---|---|---|---|
| S1 | `loan-policy-public` | minimum annual revenue | Chunks from the product sheet or eligibility policy | Semantic answers from the product sheet and the eligibility rules table | Yes |
| S2 | `loan-policy-public` | interest rate 24 months | The rate table in `rates-and-fees.md` | Top semantic answer is the rate table (answer score 0.97) | Yes |
| S3 | `loan-policy-public` | DSCR | No internal content | No semantic answers; top result is an unrelated FAQ chunk (reranker 1.90) | Yes |
| S4 | `loan-policy-staff` | DSCR | The credit manual | Two semantic answers from `credit-manual-internal.md`: the DSCR step (0.98) and the decision guide (0.97); top reranker 2.67 | Yes |

## Lessons

- A vector query always returns the nearest chunks, so every query returned all chunks (`@odata.count` 9
  or 11), even when nothing matches. Relevance shows in the reranker score and in whether semantic answers
  exist. The agent must say when the sources do not answer, rather than answer from the nearest chunk; the
  test set covers this in its out-of-scope cases.
- S3 and S4 together show the audience split works at the index level (decision D6).
