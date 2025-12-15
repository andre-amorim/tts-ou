import typer
from pathlib import Path
from dotenv import load_dotenv
import os

from parser import extract_text_from_markdown
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
):
    """
    Convert a Markdown file to MP3 audio.
    """
    # 1. Parse Markdown
    typer.echo(f"Parsing {input_file}...")
    try:
        chunks = extract_text_from_markdown(input_file)
        typer.echo(f"Extracted {len(chunks)} text chunks.")
    except Exception as e:
        typer.echo(f"Error parsing file: {e}", err=True)
        raise typer.Exit(code=1)

    # 2. Check Credentials
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        typer.echo("WARNING: GOOGLE_APPLICATION_CREDENTIALS not found in environment.", err=True)
        typer.echo("Please ensure it is set, otherwise TTS client initialization may fail.", err=True)

    # 3. Synthesize
    typer.echo("Initializing TTS client...")
    try:
        tts_client = GoogleTTS(language_code=language, voice_name=voice)
        typer.echo("Starting synthesis...")
        tts_client.synthesize(text_chunks=chunks, output_file=output_file)
        typer.echo(f"Done! Output saved to {output_file}")
    except Exception as e:
        typer.echo(f"Error during synthesis: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
