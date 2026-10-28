# dpdp-research-assistant

> **A citation-grounded regulatory research assistant for the Indian DPDP Act (2023), DPDP Rules (2025), Corrigenda, and MeitY Enforcement Timelines.**

---

## 1. Domain Context: What is DPDP and Why Was It Selected?

### What is the DPDP?
The **Digital Personal Data Protection Act, 2023 (DPDP Act)** is India's principal statutory framework governing the processing of digital personal data. It establishes rights for individuals and obligations for data processors, supported by the **DPDP Rules (2025)**, corrigenda, and Ministry of Electronics and Information Technology (MeitY) enforcement notifications.

### Core Domain Terminology
* **Data Principal:** The natural person to whom personal data relates (the citizen/user).
* **Data Fiduciary:** Any person or entity that determines the purpose and means of processing personal data (companies, banks, apps).
* **Significant Data Fiduciary (SDF):** High-impact fiduciaries subject to enhanced obligations (regular data audits, independent Data Protection Officers).
* **Data Protection Board of India (DPBI):** The statutory adjudicatory body responsible for inquiring into breaches, directing remedial action, and imposing penalties.

### Why DPDP Was Chosen (Strategic Rationale)
1. **Relevance in India:** Highly pertinent to the Indian engineering and tech ecosystem without requiring artificial financial or foreign domain jargon.
2. **Real Statutory Hierarchy:** The corpus contains distinct document tiers:
   - Primary legislation (the 2023 Act)
   - Secondary legislation (the 2025 Rules)
   - Corrections (Corrigenda)
   - Staggered commencement notices
3. **The "What It Says" vs. "When It Takes Effect" Challenge:** Standard semantic retrieval treats all text as equal. Legal compliance demands distinguishing what a provision mandates from whether it has come into legal force.
4. **Verifiable Ground Truth:** Easy to establish objective citation benchmarks and strictly test for **abstention** (declining to answer when the corpus does not provide evidence).

---

## 2. Engineering Philosophy & Working Agreement

* **Independent Competence Over Hype:** Focus on understanding plain Python foundations, data contracts, and test mechanics before introducing complex frameworks (Pydantic, Celery, FastAPI).
* **Workspace Isolation:** All source code lives in `src/dpdp/` and all tests in `tests/` to prevent interference with other workspace tracks.
* **The 5-Step Learning Loop:**
  1. Define behavior and edge cases in plain language.
  2. Write the failing test first in `tests/`.
  3. Implement the smallest working code in `src/dpdp/`.
  4. Perform the two-sentence explain-back check.
  5. Complete an independence check without hints.

---

## 3. Progress Log

### Task 1: Formatting a Source Citation (`format_citation`)
* **Source:** `src/dpdp/citations.py`
* **Tests:** `tests/test_citations.py` (3 tests passed)
* **What it does:** Formats a passage dictionary into a readable bracketed citation label (e.g., `"[DPDP Act 2023, Section 4]"`). Rejects blank or whitespace-only inputs with a `ValueError`.

### Task 2: Representing and Validating a Passage (`create_passage`)
* **Source:** `src/dpdp/passages.py`
* **Tests:** `tests/test_passages.py` (4 tests passed)
* **What it does:** Sanitizes and constructs a standardized passage dictionary containing `text`, `document`, and `section`. Validates that none of the required fields are empty or whitespace-only.

### Task 3: Deterministic Passage Identification (`generate_passage_id`)
* **Source:** `src/dpdp/passages.py`
* **Tests:** `tests/test_passages.py` (2 tests passed)
* **What it does:** Computes deterministic lowercase slug IDs (e.g. `"dpdp-act-2023:section-4"`) for reliable indexing and cross-referencing.

### Task 4: Grounded Research Snippets (`format_grounded_snippet` & `format_context_snippet`)
* **Source:** `src/dpdp/citations.py`
* **Tests:** `tests/test_citations.py` (8 tests passed)
* **What it does:** Formats cited passages for user-facing quotes (`'"Text" [Doc, Section]'`) and LLM prompt context blocks (`'[Doc, Section] "Text"'`). Reuses `format_citation` and validates non-blank text.

### Task 5: In-Memory Passage Store & Direct Lookup (`index_passages` & `get_passage`)
* **Source:** `src/dpdp/passages.py`
* **Tests:** `tests/test_passages.py` (5 tests passed)
* **What it does:** Indexes a list of passages by `passage_id` with $O(1)$ lookup and duplicate collision detection. `get_passage` retrieves by ID with defensive `KeyError` safety.

### Task 6: Optional Clause Identity (`create_passage(..., clause=...)`)
* **Source:** `src/dpdp/passages.py`
* **Tests:** `tests/test_passages.py` (5 tests passed)
* **What it does:** A passage may carry an optional `clause`. When present, `generate_passage_id` appends `:clause-<slug>` (e.g. `"dpdp-act-2023:section-8:clause-5"`) so sub-clauses of one section get distinct IDs. Passages without a clause keep the original `document:section` ID. A blank clause is rejected.

### Task 7: Document Loader (`load_document`, `load_corpus`, `summarize_corpus`)
* **Source:** `src/dpdp/loader.py`
* **Tests:** `tests/test_loader.py` (16 tests passed, including an integration test over `data/dpdp/`)
* **What it does:** Loads markdown files into standard records (`content`, `filename`, `path`, `document`, `char_count`), loads a directory in sorted order, and summarizes a corpus. Missing paths, directories-as-files and empty files raise explicit errors.

* **Current Test Status:** `43 passed` across `tests/` (citations 11, passages 16, loader 16).

---

## 4. Production Pipeline Phases & Status

- [x] **Phase 1: Core Data Contracts & Invariants (Completed — 27 tests passing across citations and passages)**
  - Canonical Passage schema & validation (`create_passage`).
  - Deterministic identification (`generate_passage_id`).
  - Source citation contracts (`format_citation`, `format_grounded_snippet`, `format_context_snippet`).
  - Collision-safe in-memory store & direct retrieval (`index_passages`, `get_passage`).

- [ ] **Phase 2: Corpus Ingestion & Document Chunking (In Progress)**
  - [x] Source document curation in `data/dpdp/` (DPDP Act 2023, Rules 2025, MeitY timeline).
  - [x] Document loader (`load_document`, `load_corpus`, `summarize_corpus`).
  - [ ] Legal boundary chunker (splitting by statutory Sections/Rules/Schedules) in `src/dpdp/chunker.py`, not yet created.
  - [ ] Transforming parsed raw sections into canonical `Passage` records.

- [ ] **Phase 3: Retrieval Engines**
  - Baseline lexical / statutory search (exact keyword & section number matching).
  - Dense vector embeddings with cosine similarity.
  - Hybrid retrieval (BM25 + Dense vector ranking).

- [ ] **Phase 4: Grounded Synthesis & Abstention**
  - Prompt context assembly with strict citations.
  - Abstention guardrails (refusing to hallucinate when corpus lacks evidence).

- [ ] **Phase 5: Evaluation Benchmark & Golden Set**
  - Factual questions with expected citations.
  - Out-of-scope questions testing abstention.
  - Automated CI/CD evaluation harness.
