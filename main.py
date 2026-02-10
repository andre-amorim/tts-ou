import typer
from pathlib import Path
from dotenv import load_dotenv
import os

from converter import InputConverter
from optimizer import TextOptimizer
from tts import GoogleTTS

# Load environment variables (for GOOGLE_APPLICATION_CREDENTIALS)
load_dotenv()

app = typer.Typer(help="TTS OU - Convert Markdown to MP3 using Google Cloud TTS")

@app.command()
def convert(
    input_file: Path = typer.Argument(..., exists=True, help="Path to input Markdown file"),
    output_file: Path = typer.Argument(..., help="Path to save output MP3 file"),
    language: str = typer.Option("en-US", help="Language code (e.g., en-US, en-GB)"),
    voice: str = typer.Option(None, help="Specific voice name (optional)"),
    optimize: bool = typer.Option(True, help="Enable AI text optimization (requires GOOGLE_API_KEY)"),
    tier: str = typer.Option("free", help="Optimization tier: 'free' (API Key), 'paid' (Vertex AI), or 'auto' (free then paid)"),
):
    """
    Convert a Markdown file to MP3 audio.
    """
    # 1. Convert Input
    typer.echo(f"Converting {input_file}...")
    try:
        converter = InputConverter()
        raw_text = converter.convert_to_markdown(input_file)
        typer.echo(f"Converted input. Size: {len(raw_text)} characters.")
    except Exception as e:
        typer.echo(f"Error converting file: {e}", err=True)
        raise typer.Exit(code=1)

    # 2. Optimize Text (Optional)
    final_text = raw_text
    is_ssml = False
    
    if optimize:
        typer.echo(f"Optimizing text with AI Agent ({tier} tier)...")
        try:
            optimizer = TextOptimizer(tier=tier)
            # If optimization is successful, the result is "fluid text". 
            final_text = optimizer.optimize(raw_text)
            typer.echo(f"Optimization complete. New size: {len(final_text)} characters.")
        except Exception as e:
            # CRITICAL: Do not proceed if optimization fails. 
            # This respects user intent and avoids unnecessary Google Cloud TTS costs for unoptimized text.
            typer.echo(f"Optimization failed: {e}", err=True)
            raise typer.Exit(code=1)

    # 3. Chunk for TTS
    # Google TTS has a limit per request (5000 bytes/chars).
    from text_utils import chunk_text
    chunks = chunk_text(final_text, limit=4500)
    typer.echo(f"Prepared {len(chunks)} chunks for TTS.")

    # 4. Check Credentials
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        typer.echo("WARNING: GOOGLE_APPLICATION_CREDENTIALS not found in environment (required for TTS).", err=True)

    # 5. Synthesize
    typer.echo("Initializing TTS client...")
    try:
        tts_client = GoogleTTS(language_code=language, voice_name=voice)
        typer.echo("Starting synthesis...")
        tts_client.synthesize(text_chunks=chunks, output_file=output_file, is_ssml=is_ssml)
        typer.echo(f"Done! Output saved to {output_file}")
    except Exception as e:
        typer.echo(f"Error during synthesis: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
