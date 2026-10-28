# ADR 0001: Statutory Corpus Hierarchy and Source Curation

## Status: Accepted

---

## Context
When designing an AI compliance research assistant for Indian privacy regulations, we needed to select the source dataset. Typical RAG demonstrations use generic web blog posts, summarized FAQs, or artificial synthetic paragraphs. 

However, regulatory compliance requires precise distinction between:
1. Primary parliamentary legislation (the DPDP Act, 2023).
2. Subordinate operational rules (the DPDP Rules, 2025).
3. Executive notification schedules and corrigenda (MeitY implementation timelines).

## Options Considered
1. **Option A: Synthetic / Summarized FAQ Corpus:** Scrape privacy blogs, law firm advisory memos, and marketing summaries.
2. **Option B: Gazette-Grounded Multi-Tier Statutory Corpus:** Ingest official gazette notifications, verbatim legal statutes, and MeitY rollout schedules in structured Markdown.

## Decision
We chose **Option B: Gazette-Grounded Multi-Tier Statutory Corpus**, housing the authentic texts in `data/dpdp/`:
- `dpdp_act_2023.md` (Acts 1–44, Chapters I–IX, Schedule of Penalties)
- `dpdp_rules_2025.md` (Operational frameworks: Notice, Consent Managers, SDF criteria)
- `meity_timeline.md` (Enforcement phases, effective dates vs enactment dates, Corrigenda)

## Why We Chose It
1. **Auditable Ground Truth:** Legal practitioners and auditors do not accept answers citing blog posts. Citations must point to actual statutory enactments (`[DPDP Act 2023, Section 8(5)]`).
2. **"What It Says" vs. "When It Takes Effect":** Indian privacy law is being rolled out in phases. A system trained only on the Act cannot warn a user whether a clause is currently in legal force. Our tiered corpus makes temporal status explicitly retrievable.
3. **Rigorous Hallucination Testing:** Real statutory text features strict terminology (*Data Principal*, *Data Fiduciary*, *Consent Manager*), making it straightforward to test for false conflation with GDPR terms.

## Trade-offs Accepted
- Official statutory text is denser and includes formal legislative drafting conventions (e.g. sub-clauses, provisos, schedules), requiring custom boundary chunking rather than naive fixed-window token slicing.
