"""Unit and integration tests for DPDP document loader."""

from pathlib import Path

import pytest

from dpdp.loader import load_corpus, load_document, summarize_corpus


def test_load_document_happy_path(tmp_path: Path):
    """Loading a valid markdown document returns the expected contract structure."""
    doc_file = tmp_path / "test_doc.md"
    doc_file.write_text("# Test Document\n\nThis is sample content for testing.", encoding="utf-8")

    doc = load_document(doc_file)

    assert isinstance(doc, dict)
    assert doc["filename"] == "test_doc.md"
    assert doc["document"] == "Test Document"
    assert "This is sample content for testing." in doc["content"]
    assert doc["char_count"] == len(doc["content"])
    assert doc["path"] == str(doc_file.resolve())


def test_load_document_extracts_title_from_first_h1(tmp_path: Path):
    """Document title is extracted from the first top-level markdown heading (# Title)."""
    doc_file = tmp_path / "act.md"
    content = "# Digital Personal Data Protection Act, 2023\n\nChapter I..."
    doc_file.write_text(content, encoding="utf-8")

    doc = load_document(doc_file)
    assert doc["document"] == "Digital Personal Data Protection Act, 2023"


def test_load_document_title_fallback_when_no_h1(tmp_path: Path):
    """When no top-level # heading is present, fallback to formatted filename."""
    doc_file = tmp_path / "dpdp_rules_2025.md"
    doc_file.write_text("No top-level heading here, just raw text.", encoding="utf-8")

    doc = load_document(doc_file)
    assert doc["document"] == "Dpdp Rules 2025"


def test_load_document_preserves_unicode(tmp_path: Path):
    """Special characters such as Indian Rupee sign (₹) and Em-dashes must load cleanly."""
    doc_file = tmp_path / "penalties.md"
    content = "# Penalties\n\nMaximum penalty: ₹250 crore — statutory limit."
    doc_file.write_text(content, encoding="utf-8")

    doc = load_document(doc_file)
    assert "₹250 crore — statutory limit." in doc["content"]


def test_load_document_missing_file_raises_filenotfound():
    """Attempting to load a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_document("data/dpdp/non_existent_file.md")


def test_load_document_directory_path_raises_isadirectoryerror(tmp_path: Path):
    """Passing a directory path to load_document raises IsADirectoryError."""
    with pytest.raises(IsADirectoryError):
        load_document(tmp_path)


def test_load_document_zero_bytes_raises_valueerror(tmp_path: Path):
    """A 0-byte file raises ValueError to prevent empty documents entering the pipeline."""
    empty_file = tmp_path / "empty.md"
    empty_file.write_text("", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_document(empty_file)


def test_load_document_whitespace_only_raises_valueerror(tmp_path: Path):
    """A file containing only spaces and newlines raises ValueError."""
    whitespace_file = tmp_path / "blank.md"
    whitespace_file.write_text("   \n\n\t  \r\n   ", encoding="utf-8")

    with pytest.raises(ValueError, match="empty"):
        load_document(whitespace_file)


def test_load_corpus_happy_path(tmp_path: Path):
    """load_corpus loads all markdown files in a directory sorted deterministically by filename."""
    (tmp_path / "b_doc.md").write_text("# Doc B\n\nContent B", encoding="utf-8")
    (tmp_path / "a_doc.md").write_text("# Doc A\n\nContent A", encoding="utf-8")
    (tmp_path / "ignored.txt").write_text("Should not be loaded", encoding="utf-8")

    docs = load_corpus(tmp_path)

    assert len(docs) == 2
    assert docs[0]["filename"] == "a_doc.md"
    assert docs[0]["document"] == "Doc A"
    assert docs[1]["filename"] == "b_doc.md"
    assert docs[1]["document"] == "Doc B"


def test_load_corpus_missing_directory_raises_filenotfound():
    """Non-existent corpus directory raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        load_corpus("data/non_existent_directory")


def test_load_corpus_file_path_raises_notadirectoryerror(tmp_path: Path):
    """Passing a file path to load_corpus raises NotADirectoryError."""
    file_path = tmp_path / "single.md"
    file_path.write_text("# Single\n\nContent", encoding="utf-8")

    with pytest.raises(NotADirectoryError):
        load_corpus(file_path)


def test_load_corpus_empty_directory_raises_valueerror(tmp_path: Path):
    """A directory with no markdown files raises ValueError."""
    with pytest.raises(ValueError, match="No markdown documents found"):
        load_corpus(tmp_path)


def test_load_corpus_real_dpdp_directory():
    """Integration test: Real data/dpdp directory must load exactly 3 valid statutory documents."""
    corpus_dir = Path("data/dpdp")
    assert corpus_dir.exists(), "data/dpdp directory must exist"

    docs = load_corpus(corpus_dir)

    assert len(docs) == 3
    filenames = [d["filename"] for d in docs]
    assert filenames == ["dpdp_act_2023.md", "dpdp_rules_2025.md", "meity_timeline.md"]

    # Verify each document loaded with authentic non-empty content and proper title
    doc_titles = {d["filename"]: d["document"] for d in docs}
    assert doc_titles["dpdp_act_2023.md"] == "Digital Personal Data Protection Act, 2023"
    assert doc_titles["dpdp_rules_2025.md"] == "Digital Personal Data Protection Rules, 2025"
    assert doc_titles["meity_timeline.md"] == "MeitY Implementation Roadmap and Corrigenda"

    # Verify characters were loaded
    for d in docs:
        assert d["char_count"] > 1000

def test_summarise_corpus_valid():
    # 1. Load the list of documents
    corpus = load_corpus("data/dpdp")

    # 2. Generate the audit summary dictionary
    summary = summarize_corpus(corpus)

    # 3. Assert on the summary dictionary keys
    assert summary["total_documents"] == 3
    assert summary["total_characters"] > 30000
    assert len(summary["document_names"]) == 3

def test_summarize_corpus_empty_raises_valueerror():
    p1 = []

    with pytest.raises(ValueError, match="empty"):
        summarize_corpus(p1)

def test_summarize_corpus_invalid_record_raises_valueerror():
    d1 = [{"content": "hello"}]

    with pytest.raises(ValueError, match="missing keys"):
        summarize_corpus(d1)
