import google.generativeai as genai
import os
from text_utils import chunk_text

class TextOptimizer:
    def __init__(self, model_name="gemini-1.5-flash"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def optimize(self, text: str) -> str:
        """
        Rewrites the text to be more fluid and suitable for speech.
        """
        if not self.api_key:
            print("Warning: GOOGLE_API_KEY not found. Skipping optimization.")
            return text

        # Chunk size for optimization (output limit is the constraint)
        # 15000 chars is roughly 3k-4k tokens. Output limit is ~8k tokens.
        # This is safe.
        chunks = chunk_text(text, limit=15000)
        optimized_chunks = []

        total_chunks = len(chunks)
        print(f"Optimizing {total_chunks} chunks of text...")

        for i, chunk in enumerate(chunks):
            try:
                print(f"Optimizing chunk {i+1}/{total_chunks}...")
                response = self.model.generate_content(
                    f"""Rewrite the following text to be read aloud (Text-to-Speech).
MAKE IT FLUID, NATURAL, AND ENGAGING.
Remove any page numbers, citations, footnotes, tables, and external links.
Do not include any standard markdown formatting like bold or italics unless it helps with emphasis in speech.
Do not add any preamble like 'Here is the text'. Just output the rewritten text.

Text:
{chunk}
"""
                )
                optimized_chunks.append(response.text)
            except Exception as e:
                print(f"Error optimizing chunk {i+1}: {e}")
                optimized_chunks.append(chunk) # Fallback to original

        return " ".join(optimized_chunks)
