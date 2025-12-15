from typing import List

def chunk_text(text: str, limit: int) -> List[str]:
    """
    Splits text into chunks respecting the character limit.
    Tries to split on sentence boundaries if possible.
    """
    chunks = []
    current_chunk = ""

    # Simple sentence splitting, can be improved
    sentences = text.split('. ') 
    
    for i, sentence in enumerate(sentences):
        # Re-add the period that was removed by split (unless it's the last empty one)
        if i < len(sentences) - 1 or sentence.strip():
             sentence += ". "
        
        if len(current_chunk) + len(sentence) <= limit:
            current_chunk += sentence
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
            
            # If a single sentence is huge, strict chop it
            while len(current_chunk) > limit:
                 chunks.append(current_chunk[:limit])
                 current_chunk = current_chunk[limit:]

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks
