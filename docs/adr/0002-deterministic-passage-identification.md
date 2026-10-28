# ADR 0002: Deterministic Slug Passage IDs vs. Random UUIDs

## Status: Accepted

---

## Context
In a RAG retrieval system, every indexed passage requires a unique identifier. We evaluated whether to assign auto-incrementing integers, random UUIDs (`uuid.uuid4()`), or deterministic semantic slugs computed directly from the document and statutory section.

## Options Considered
1. **Option A: Random UUIDs (`uuid4`):** Generate a 128-bit random hexadecimal string for each passage upon ingestion.
2. **Option B: Auto-incrementing Integers:** Number passages sequentially `1, 2, 3...` during the indexing loop.
3. **Option C: Deterministic Semantic Slugs:** Compute canonical lowercase slugs from document and statutory section names (e.g. `dpdp-act-2023:section-4`).

## Decision
We chose **Option C: Deterministic Semantic Slugs** implemented in `generate_passage_id(document, section)`.

## Why We Chose It
1. **Idempotence & Cache Stability:** If the corpus is re-ingested or re-indexed across worker instances, the passage ID remains identical. This prevents cache invalidation of downstream evaluation datasets and golden citation benchmarks.
2. **Auditable Evaluation Assertions:** In the planned evaluation harness (`evals/dpdp/`, golden dataset not yet written), an expected citation target can assert against `dpdp-act-2023:section-8` directly. With random UUIDs, assertions require fragile dynamic lookups.
3. **Collision Detection:** Deterministic keys enable instant detection if the chunker accidentally produces two distinct passages with identical section identifiers, catching indexing bugs before deployment.

## Trade-offs Accepted
- If a statute has multiple sub-clauses within the same section that are split into separate passages, the slug computation must append sub-clause identifiers to guarantee uniqueness. Implemented: a passage may carry an optional `clause`, and `generate_passage_id` then appends `:clause-<slug>` (e.g. `dpdp-act-2023:section-8:clause-5`). Passages without a clause keep the plain `document:section` ID.
- IDs are stable only while the document title and section/clause labels are stable. Renaming a document (the title comes from its first H1) changes every ID derived from it.
