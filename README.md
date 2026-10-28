# dpdp

A citation-grounded research assistant for the Indian DPDP statutory ecosystem (DPDP Act 2023, DPDP Rules 2025, MeitY enforcement timelines). Answers must carry a verifiable statutory citation, and the system must abstain when the corpus cannot answer.

**Status: early build.** Working today: the document loader, the passage contract (with deterministic IDs, optional clause level) and citation formatting. Not built yet: the statutory chunker, retrieval, the AI gateway with abstention, and the evaluation harness. See `PROGRESS.md` for the roadmap.

## Run the tests

```bash
uv sync
uv run pytest tests
```

Tests run offline and need no API keys.

## Layout

| Path | What is there |
| :--- | :--- |
| `src/dpdp/` | `loader.py`, `passages.py`, `citations.py`, `REFERENCE.md` |
| `tests/` | pytest suite (43 tests) |
| `data/dpdp/` | Statute texts: Act 2023, Rules 2025, MeitY timeline |
| `docs/architecture/` | Problem statement and system design |
| `docs/adr/` | Architecture decision records |
| `evals/dpdp/` | Empty for now; the golden dataset will go here |
| `PROGRESS.md` | Roadmap, evidence log and handoff brief |
| `AGENTS.md` | Operating rules for AI assistants in this repo |

`skills/` and `portfolio_workflow_guide.md` are local-only and git-ignored.
