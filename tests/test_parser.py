from parser import extract_text_from_markdown, chunk_text

def test_chunking():
    text = "Sentence one. " * 500
    chunks = chunk_text(text, limit=100)
    for chunk in chunks:
        assert len(chunk) <= 100
    
    assert len(chunks) > 0

def test_markdown_extraction(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.md"
    p.write_text("# Header\n\nSome **bold** text.\n\n- Item 1\n- Item 2", encoding="utf-8")
    
    chunks = extract_text_from_markdown(p)
    full_text = " ".join(chunks)
    
    assert "Header" in full_text
    assert "Some bold text." in full_text
    assert "Item 1" in full_text
