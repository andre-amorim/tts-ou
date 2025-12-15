from converter import InputConverter
import pytest

def test_input_converter_markdown(tmp_path):
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test.md"
    p.write_text("# Header\n\nSome **bold** text.\n\n- Item 1\n- Item 2", encoding="utf-8")
    
    converter = InputConverter()
    text = converter.convert_to_markdown(p)
    
    # MarkItDown output might differ slightly in formatting, but should contain the text
    assert "Header" in text
    assert "Some **bold** text" in text or "Some bold text" in text
    assert "Item 1" in text
