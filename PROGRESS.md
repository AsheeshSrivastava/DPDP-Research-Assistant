# Production RAG Engineering & Portfolio Progress Tracker

> **Governing Standards:**
> - Portfolio Blueprint: [`portfolio_workflow_guide.md`](portfolio_workflow_guide.md) (7 Macro Phases)
> - Mentorship Facilitator: [`skills/systems-architect-mentor/SKILL.md`](skills/systems-architect-mentor/SKILL.md) (6-Step Loop)
> - Project Operating Agreement: [`AGENTS.md`](AGENTS.md)
>
> `portfolio_workflow_guide.md` and `skills/` are local-only (git-ignored); a fresh clone will not have them. There is no separate session-manager skill; the handoff procedure is in `AGENTS.md`.

---

## 1. Project Context & Real-World Domain

* **Project Repository:** `dpdp` (Document Research Assistant for Indian DPDP Framework)
* **Domain Context:** Indian Digital Personal Data Protection statutory ecosystem:
  - Primary Legislation: *DPDP Act 2023 (Act No. 22 of 2023)*
  - Secondary Legislation: *DPDP Rules 2025*
  - Phased Rollout & Corrigenda: *MeitY Enforcement Timelines*
* **Core Non-Functional Targets:**
  - **Latency:** $< 1.5$s per regulatory retrieval and grounded synthesis query
  - **Zero-Hallucination & Abstention:** Strict citation requirement (`[Document, Section]`); zero unsupported assertions; explicit abstention when query falls outside the statutory corpus
  - **Unit Economics:** Operating budget capped at $< \$0.005$ per compliance query via local retrieval and prompt optimization
  - **Zero-Key Local Execution:** Full end-to-end testing and in-memory indexing runnable without cloud API keys (`MOCK_AI=true`)

---

## 2. Active Roadmap State

* **Playbook Phase:** `Phase 3: Core Logic & Mock Engine` (in parallel with Playbook Phases 1 & 2 documentation alignment)
* **Numbering note:** "Playbook Phase N" is the 7-phase portfolio playbook. The "Phase N: ..." labels in the evidence log below are this project's own build units (contracts, ingestion, chunking) and are a different scheme.
* **Active Subsystem:** `Unit 2, Task 1: The Raw Corpus & Document Loader` (built; audit/defense steps pending)
* **Active Components:**
  - `src/dpdp/loader.py`: `load_document`, `load_corpus`, and `summarize_corpus`
  - `tests/test_loader.py`: Unit and integration test suite
* **Upcoming Component:** `Unit 2, Task 2: Statutory Boundary Chunker` (`src/dpdp/chunker.py`, not yet created)
* **Test Suite Status:** 43 tests passing (`tests/test_citations.py` (11), `tests/test_passages.py` (16), `tests/test_loader.py` (16))
* **Placeholders:** `evals/dpdp/` exists but is empty (golden dataset to be created later).

---

## 3. Unit & Skill Evidence Log

| Phase / Unit | Component | Implemented Functions / Contracts | Verification Evidence | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Contracts** | Citations (`citations.py`) | `format_citation`, `format_grounded_snippet`, `format_context_snippet` | 11 tests passing in `test_citations.py` | Complete |
| **Phase 1: Contracts** | Passages (`passages.py`) | `create_passage` (optional `clause`), `generate_passage_id` (`doc:section[:clause-x]`), `index_passages`, `get_passage` | 16 tests passing in `test_passages.py` | Complete |
| **Phase 2: Ingestion** | Corpus (`data/dpdp/`) | `dpdp_act_2023.md`, `dpdp_rules_2025.md`, `meity_timeline.md` | Authentic full statutory texts verified | Complete |
| **Phase 2: Ingestion** | Loader (`loader.py`) | `load_document`, `load_corpus` | 13 tests passing in `test_loader.py` | Complete |
| **Phase 2: Ingestion** | Companion Audit (`loader.py`) | `summarize_corpus` | 3 tests passing in `test_loader.py` (coded in Zed) | Complete |
| **Phase 2: Chunking** | Chunker (`chunker.py`) | `chunk_document_by_section`, `chunk_corpus` | Statutory boundary chunking spec | In Progress |

---

## 4. Portfolio Deliverables Registry

| Playbook Phase | Deliverable Asset | Location | Status |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Problem Statement & Numeric Constraints | `docs/architecture/01-problem-statement.md` | Complete |
| **Phase 2** | System Design Diagram & Core ADRs | `docs/architecture/02-system-design.md`, `docs/adr/` | Complete |
| **Phase 3** | Core Statutory Logic & Zero-Key Ingestion Engine | `src/dpdp/`, `tests/` | Active (43 tests passing) |
| **Phase 4** | AI Gateway, Failure Recovery & Low-Confidence Abstention | `docs/architecture/03-resilience-and-fallbacks.md`, `src/dpdp/gateway/` | Planned |
| **Phase 5** | Golden Dataset & Automated Evaluation Harness | `evals/dpdp/golden_dataset.json`, `evals/dpdp/run_evals.py` (folder exists, empty) | Planned |
| **Phase 6** | FinOps & Unit Economics Model | `docs/architecture/economics.md` | Planned |
| **Phase 7** | Executive 2-Minute README & Architecture Diagram | `README.md` (currently empty) | Planned |

---

## 5. Next Session Handoff Brief

* **Immediate Goal:** Launch **Unit 2, Task 2: Statutory Boundary Chunker** (`src/dpdp/chunker.py`).
* **Opening Step:** Step 1 (Behavior & Edge Cases in plain English) — parse sections/rules/schedules into canonical passage dictionaries.
* **Prompt for New Session:**
  > *"I am resuming work on the DPDP Production RAG project. Please inspect PROGRESS.md and continue with Unit 2, Task 2: Statutory Boundary Chunker."*
