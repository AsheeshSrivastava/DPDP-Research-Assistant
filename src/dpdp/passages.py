def _slug(value: str) -> str:
    return value.strip().lower().replace(" ", "-")


def create_passage(text: str, document: str, section: str, clause: str | None = None) -> dict:
    """Build a canonical passage dict.

    `clause` is optional. It is stored only when given, so a section-level
    passage keeps the same shape (and ID) as before. A blank clause is rejected.
    """

    clean_text = text.strip()
    clean_document = document.strip()
    clean_section = section.strip()

    if not clean_text or not clean_document or not clean_section:
        raise ValueError("text, document or section cannot be empty")

    passage = {"text": clean_text,
        "document": clean_document,
        "section" : clean_section,
    }

    if clause is not None:
        clean_clause = clause.strip()
        if not clean_clause:
            raise ValueError("clause cannot be blank when provided")
        passage["clause"] = clean_clause

    return passage

def generate_passage_id(passage: dict) -> str:
    """Return the deterministic slug ID: `document:section[:clause-x]`."""

    passage_id = _slug(passage["document"]) + ":" + _slug(passage["section"])

    clause = passage.get("clause")
    if clause is not None:
        passage_id += ":clause-" + _slug(clause)

    return passage_id


def index_passages(passages: list[dict]) -> dict[str, dict]:
    index = {}

    for passage in passages:
        passage_id = generate_passage_id(passage)
        if passage_id in index:
            raise ValueError(f"Duplicate passage ID: {passage_id}")
        index[passage_id] = passage

    return index


def get_passage(index: dict[str, dict], passage_id: str) -> dict:
    clean_id = passage_id.strip()

    if clean_id not in index:
        raise KeyError(f"Passage ID not found: {clean_id}")

    return index[clean_id]




if __name__ == "__main__":
    text = "Hello World"
    document = "DPDP 2025 Act"
    section = "section 5"
    passage = create_passage(text, document, section)
    passage_id = generate_passage_id(passage)
    index = index_passages([passage])
    ret_passage = get_passage(index, passage_id)
    print(passage)
    print()
    print(passage_id)
    print()
    print(index)
    print()
    print(ret_passage)
