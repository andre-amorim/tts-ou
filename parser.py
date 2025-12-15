import markdown
from bs4 import BeautifulSoup
from pathlib import Path
from typing import List

# Google TTS limit is 5000 characters. We'll stick to a safe limit.
CHUNK_SIZE = 4500

def extract_text_from_markdown(file_path: Path) -> List[str]:
    """
    Reads a Markdown file, converts it to text, and chunks it.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    # Read Markdown content
    with open(file_path, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert to HTML
    html = markdown.markdown(md_content)

    # Extract text using BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator=" ")

    # Normalize whitespace
    text = " ".join(text.split())

    return chunk_text(text)

def chunk_text(text: str, limit: int = CHUNK_SIZE) -> List[str]:
    """
    Splits text into chunks respecting the character limit.
    Tries to split on sentence boundaries if possible.
    """
    chunks = []
    current_chunk = ""

    sentences = text.split('. ') # Simple sentence splitting

    for sentence in sentences:
        # Re-add the period that was removed by split (if it's not the last one purely empty)
        if sentence: 
             sentence += ". "
        
        if len(current_chunk) + len(sentence) <= limit:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
            
            # If a single sentence is huge (unlikely but possible), strict chop it
            while len(current_chunk) > limit:
                 chunks.append(current_chunk[:limit])
                 current_chunk = current_chunk[limit:]

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
