import pytest

from dpdp.passages import (
    create_passage,
    generate_passage_id,
    get_passage,
    index_passages,
)


def test_create_passage_returns_valid_dict():

    result = create_passage(
        text="The provisions of this Act shall apply to...",
        document="DPDP Act 2023",
        section="Section 4",
    )

    assert result == {"text": "The provisions of this Act shall apply to...",
        "document": "DPDP Act 2023",
        "section": "Section 4",
    }


def test_create_passage_rejects_blank_text():

    sample_text_1 =  " "
    sample_document_1 = "DPDP Act 2023"
    sample_section_1 = "Section 4"

    with pytest.raises(ValueError):
        create_passage(sample_text_1, sample_document_1, sample_section_1)


def test_create_passage_rejects_blank_document():

    sample_text_2 =  "The provisions of this Act shall apply to..."
    sample_document_2 = " "
    sample_section_2 = "Section 4"

    with pytest.raises(ValueError):
        create_passage(sample_text_2, sample_document_2, sample_section_2)


def test_create_passage_rejects_blank_section():

    sample_text_3 =  "The provisions of this Act shall apply to..."
    sample_document_3 = "DPDP Act 2023"
    sample_section_3 = " "

    with pytest.raises(ValueError):
        create_passage(sample_text_3, sample_document_3, sample_section_3)


def test_passage_id_creates_slug():

    passage = create_passage(
        text="The provisions of this Act shall apply to...",
        document="DPDP Act 2023",
        section="Section 4",
    )

    result = generate_passage_id(passage)

    assert result == "dpdp-act-2023:section-4"


def test_generate_passage_id_strips_surrounding_whitespace():
    dirty_passage = {
        "text": "The provisions of this Act...",
        "document": "  DPDP Act 2023  ",
        "section": "  Section 4  ",
    }

    result = generate_passage_id(dirty_passage)

    assert result == "dpdp-act-2023:section-4"


def test_index_passages_stores_by_id():
    p1 = create_passage(
        text="A Data Fiduciary shall protect personal data...",
        document="DPDP Act 2023",
        section="Section 4",
    )
    p2 = create_passage(
        text="Personal data may be processed only with consent...",
        document="DPDP Act 2023",
        section="Section 5",
    )

    index = index_passages([p1, p2])

    assert len(index) == 2
    assert index["dpdp-act-2023:section-4"] == p1
    assert index["dpdp-act-2023:section-5"] == p2


def test_index_passages_empty_list_returns_empty_dict():
    assert index_passages([]) == {}


def test_index_passages_rejects_duplicate_id():
    p1 = create_passage(
        text="First draft text...",
        document="DPDP Act 2023",
        section="Section 4",
    )
    p2 = create_passage(
        text="Duplicate draft text...",
        document="DPDP Act 2023",
        section="Section 4",
    )

    with pytest.raises(ValueError, match="Duplicate passage ID"):
        index_passages([p1, p2])

def test_create_passage_without_clause_has_no_clause_key():
    passage = create_passage("Text...", "DPDP Act 2023", "Section 8")
    assert "clause" not in passage


def test_create_passage_stores_clean_clause():
    passage = create_passage("Text...", "DPDP Act 2023", "Section 8", clause="  (5)  ")
    assert passage["clause"] == "(5)"


def test_create_passage_rejects_blank_clause():
    with pytest.raises(ValueError, match="clause"):
        create_passage("Text...", "DPDP Act 2023", "Section 8", clause="  ")


def test_generate_passage_id_appends_clause_slug():
    passage = create_passage("Text...", "DPDP Act 2023", "Section 8", clause="5")
    assert generate_passage_id(passage) == "dpdp-act-2023:section-8:clause-5"


def test_clauses_of_same_section_get_distinct_ids():
    p1 = create_passage("First...", "DPDP Act 2023", "Section 8", clause="4")
    p2 = create_passage("Second...", "DPDP Act 2023", "Section 8", clause="5")
    index = index_passages([p1, p2])
    assert set(index) == {"dpdp-act-2023:section-8:clause-4", "dpdp-act-2023:section-8:clause-5"}


def test_get_passage_returns_matching_passage():
    p1 = create_passage(
        text="A Data Fiduciary shall protect personal data...",
        document="DPDP Act 2023",
        section="Section 4",
    )
    index = index_passages([p1])
    retrieved = get_passage(index, "dpdp-act-2023:section-4")
    assert retrieved == p1


def test_get_passage_raises_key_error_when_missing():
    index = {}
    with pytest.raises(KeyError, match="Passage ID not found"):
        get_passage(index, "non-existent-id")
