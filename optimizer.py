import google.generativeai as genai
from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel as VertexGenerativeModel
import os
import hashlib
from pathlib import Path
from text_utils import chunk_text

class TextOptimizer:
    def __init__(self, model_name="gemini-3-flash-preview", tier="free"):
        self.model_name = model_name
        self.tier = tier
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        
        # Configure Free Tier
        if self.api_key:
            genai.configure(api_key=self.api_key)
        self.free_model = genai.GenerativeModel(self.model_name)

        # Configure Paid Tier (Vertex AI)
        if self.creds_path:
            # Vertex AI uses the project ID from the environment or creds
            # We assume the user has configured the environment correctly
            vertexai.init(project=None, location="us-central1")
        # Note: Model names in Vertex AI sometimes differ. 
        # For simplicity, we assume the user provides a compatible name or we map it.
        self.vertex_model = VertexGenerativeModel("gemini-1.5-flash-002") # Using a stable Vertex model

        self.cache_dir = Path(".cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_prompt(self, chunk: str) -> str:
        return f"""Rewrite the following text to be read aloud (Text-to-Speech).
MAKE IT FLUID, NATURAL, AND ENGAGING.
Remove any page numbers, citations, footnotes, tables, and external links.
Do not include any standard markdown formatting like bold or italics unless it helps with emphasis in speech.
Do not add any preamble like 'Here is the text'. Just output the rewritten text.

Text:
{chunk}
"""

    def optimize(self, text: str) -> str:
        """
        Rewrites the text using the specified tier (free, paid, or auto).
        """
        chunks = chunk_text(text, limit=15000)
        optimized_chunks = []
        total_chunks = len(chunks)
        
        current_tier = "free" if self.tier in ["free", "auto"] else "paid"
        print(f"Optimizing {total_chunks} chunks using {self.tier} tier logic...")

        for i, chunk in enumerate(chunks):
            chunk_hash = hashlib.md5(chunk.encode('utf-8')).hexdigest()
            cache_file = self.cache_dir / f"{chunk_hash}.txt"

            if cache_file.exists():
                print(f"Loading chunk {i+1}/{total_chunks} from cache...")
                optimized_chunks.append(cache_file.read_text(encoding='utf-8'))
                continue

            # Optimization Logic
            success = False
            while not success:
                try:
                    if current_tier == "free":
                        if not self.api_key:
                            raise ValueError("GOOGLE_API_KEY missing for free tier.")
                        
                        print(f"Optimizing chunk {i+1}/{total_chunks} (Free Tier)...")
                        response = self.free_model.generate_content(self._get_prompt(chunk))
                        optimized_text = response.text
                    else:
                        print(f"Optimizing chunk {i+1}/{total_chunks} (Paid/Vertex Tier)...")
                        response = self.vertex_model.generate_content(self._get_prompt(chunk))
                        optimized_text = response.text

                    cache_file.write_text(optimized_text, encoding='utf-8')
                    optimized_chunks.append(optimized_text)
                    success = True

                except Exception as e:
                    # Check for rate limit (429) to handle auto-switching
                    if "429" in str(e) and self.tier == "auto" and current_tier == "free":
                        print(f"\n[!] Free tier quota exceeded at chunk {i+1}. Switching to PAID tier to continue...")
                        current_tier = "paid"
                        continue # Retry the same chunk with paid tier
                    else:
                        # If it's not a rate limit issue, or we are already in paid/manual mode, fail.
                        raise RuntimeError(f"Error optimizing chunk {i+1} on {current_tier} tier: {e}")

        return " ".join(optimized_chunks)
