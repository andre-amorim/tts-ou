from pathlib import Path
from markitdown import MarkItDown

class InputConverter:
    def __init__(self):
        self._md = MarkItDown()

    def convert_to_markdown(self, input_file: Path) -> str:
        """
        Converts the input file (PDF, DOCX, EPUB, HTML, etc.) to Markdown text.
        """
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")

        try:
            # MarkItDown determines format by extension or file content
            result = self._md.convert(str(input_file))
            return result.text_content
        except Exception as e:
            raise RuntimeError(f"Failed to convert {input_file.name}: {e}")
