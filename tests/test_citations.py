import pytest

from dpdp.citations import (
    format_citation,
    format_context_snippet,
    format_grounded_snippet,
)


def test_format_citation_returns_bracketed_label():
    sample = {"document": "DPDP Act 2023", "section": "Section 4"}

    result = format_citation(sample)

    assert result == "[DPDP Act 2023, Section 4]"

def test_format_citation_rejects_blank_section():
    bad_sample = {"document": "DPDP Act 2023", "section": "   "}

    with pytest.raises(ValueError):
        format_citation(bad_sample)

def test_format_citation_rejects_blank_document():
    bad_sample_2 = {"document": "  ", "section": "Section 4"}

    with pytest.raises(ValueError):
        format_citation(bad_sample_2)

def test_format_grounded_snippet_success():

    sample_2 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "DPDP Act 2023",
        "section": "Section 4"
    }

    result_2 = format_grounded_snippet(sample_2)

    assert result_2 == '"Personal data may be processed only for a lawful purpose." [DPDP Act 2023, Section 4]'

def test_format_grounded_snippet_rejects_blank_text():

    sample_3 = {"text": "",
        "document": "DPDP Act 2023",
        "section": "Section 4"
    }

    with pytest.raises(ValueError):
            format_grounded_snippet(sample_3)


def test_format_grounded_snippet_rejects_blank_document():

    sample_4 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "",
        "section": "Section 4"
    }

    with pytest.raises(ValueError):
            format_grounded_snippet(sample_4)


def test_format_grounded_snippet_rejects_blank_section():

    sample_5 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "DPDP Act 2023",
        "section": ""
    }

    with pytest.raises(ValueError):
            format_grounded_snippet(sample_5)


def test_format_context_snippet_success():

    sample_6 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "DPDP Act 2023",
        "section": "Section 4"
    }

    result_6 = format_context_snippet(sample_6)

    assert result_6 == '[DPDP Act 2023, Section 4] "Personal data may be processed only for a lawful purpose."'

def test_format_context_snippet_success_blank_text():

    sample_7 = {"text": "",
        "document": "DPDP Act 2023",
        "section": "Section 4"
    }

    with pytest.raises(ValueError):
            format_context_snippet(sample_7)


def test_format_context_snippet_success_blank_document():

    sample_8 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "",
        "section": "Section 4"
    }

    with pytest.raises(ValueError):
            format_context_snippet(sample_8)


def test_format_context_snippet_success_blank_section():

    sample_9 = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "DPDP Act 2023",
        "section": ""
    }

    with pytest.raises(ValueError):
            format_context_snippet(sample_9)
