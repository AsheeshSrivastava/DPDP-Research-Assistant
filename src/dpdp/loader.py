"""Document loader for DPDP statutory documents and raw corpus files."""

from pathlib import Path


def _extract_title(content: str, filename: str) -> str:
    """Extract human-readable document title from the first H1 header or fallback to filename.

    Args:
        content: The text content of the markdown file.
        filename: The filename (e.g., 'dpdp_act_2023.md').

    Returns:
        The extracted title string.
    """
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            title = stripped[2:].strip()
            if title:
                return title

    # Fallback to cleaned filename stem (e.g. 'dpdp_rules_2025' -> 'Dpdp Rules 2025')
    stem = Path(filename).stem
    return stem.replace("_", " ").title()


def load_document(file_path: str | Path) -> dict:
    """Load a markdown document safely from disk and return its standardized record.

    Args:
        file_path: Path to the target markdown file.

    Returns:
        A dictionary containing:
            - content: raw document text
            - filename: basename of the file
            - path: resolved absolute path string
            - document: extracted or inferred document title
            - char_count: character length of content

    Raises:
        FileNotFoundError: If the target file path does not exist.
        IsADirectoryError: If the path points to a directory instead of a file.
        ValueError: If the file is 0-byte or contains only whitespace.
    """
    path = Path(file_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Document file does not exist: {path}")

    if path.is_dir():
        raise IsADirectoryError(f"Expected a file path, but received a directory: {path}")

    content = path.read_text(encoding="utf-8")

    if not content.strip():
        raise ValueError(f"Document is empty: {path}")

    title = _extract_title(content, path.name)

    return {
        "content": content,
        "filename": path.name,
        "path": str(path),
        "document": title,
        "char_count": len(content),
    }


def load_corpus(dir_path: str | Path) -> list[dict]:
    """Load and return all markdown documents from a directory deterministically.

    Args:
        dir_path: Path to the directory containing markdown files.

    Returns:
        List of standardized document records, sorted alphabetically by filename.

    Raises:
        FileNotFoundError: If the directory does not exist.
        NotADirectoryError: If the path points to a file instead of a directory.
        ValueError: If no markdown (.md) documents are found in the directory.
    """
    path = Path(dir_path).resolve()

    if not path.exists():
        raise FileNotFoundError(f"Corpus directory does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Expected a directory, but received a file: {path}")

    md_files = sorted(
        [f for f in path.iterdir() if f.is_file() and f.suffix.lower() == ".md"],
        key=lambda p: p.name.lower(),
    )

    if not md_files:
        raise ValueError(f"No markdown documents found in directory: {path}")

    return [load_document(f) for f in md_files]

def summarize_corpus(corpus: list[dict]) -> dict:
    """Summarize an ingested corpus with key audit metrics.

    Args:
        corpus: List of loaded document dictionaries.

    Returns:
        dict containing:
            - total_documents: int
            - total_characters: int
            - document_names: list[str]

    Raises:
        ValueError: If corpus is not a list, is empty, or any document record
                    is missing 'document' or 'char_count'.
    """
    if not corpus:
            raise ValueError("Invalid document: empty")
    total_characters = 0
    document_names = []

    for doc in corpus:
        if "document" not in doc or "char_count" not in doc:
            raise ValueError("Invalid document record: missing keys")

        total_characters += doc["char_count"]
        document_names.append(doc["document"])

    return {"total_documents": len(corpus),
        "total_characters": total_characters,
        "document_names": document_names,
        }
