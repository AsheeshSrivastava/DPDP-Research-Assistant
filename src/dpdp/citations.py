def format_citation(passage):
    document_file = passage["document"].strip()
    document_section = passage["section"].strip()

    if not document_section or not document_file:
        raise ValueError("Document and Section cannot be blank")

    return f"[{document_file}, {document_section}]"


def format_grounded_snippet(passage: dict) -> str:
    document_text = passage["text"].strip()
    document_file_2 = passage["document"].strip()
    document_section_2 = passage["section"].strip()

    if not document_text or not document_file_2 or not document_section_2:
        raise ValueError("Text, Document and Section cannot be blank")

    #grounded_snippet = f'"{document_text}" [{document_file_2}, {document_section_2}]'
    grounded_snippet = f'"{document_text}" {format_citation(passage)}'

    return grounded_snippet


def format_context_snippet(passage: dict) -> str:
    document_text = passage["text"].strip()
    document_file_2 = passage["document"].strip()
    document_section_2 = passage["section"].strip()

    if not document_text or not document_file_2 or not document_section_2:
        raise ValueError("Text, Document and Section cannot be blank")

    #grounded_snippet = f'"{document_text}" [{document_file_2}, {document_section_2}]'
    grounded_snippet = f'{format_citation(passage)} "{document_text}"'

    return grounded_snippet



if __name__ == "__main__":
    sample = {"text": "Personal data may be processed only for a lawful purpose.",
        "document": "DPDP Act 2023",
        "section": "Section 4"
    }
    result = format_citation(sample)
    result_2 = format_grounded_snippet(sample)
    print()
    print(result)
    print()
    print(result_2)
