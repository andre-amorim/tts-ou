from text_utils import chunk_text

def test_chunking():
    text = "Sentence one. " * 500
    chunks = chunk_text(text, limit=100)
    for chunk in chunks:
        assert len(chunk) <= 100
    
    assert len(chunks) > 0
