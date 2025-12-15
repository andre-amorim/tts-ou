from pathlib import Path
from typing import List
from google.cloud import texttospeech

class GoogleTTS:
    def __init__(self, language_code: str = "en-US", voice_name: str = None):
        self.client = texttospeech.TextToSpeechClient()
        self.language_code = language_code
        self.voice_name = voice_name

    def synthesize(self, text_chunks: List[str], output_file: Path, is_ssml: bool = False):
        """
        Synthesizes audio from text chunks and saves to a single MP3 file.
        """
        combined_audio = b""

        for i, chunk in enumerate(text_chunks):
            if not chunk.strip():
                continue
            
            if is_ssml:
                input_text = texttospeech.SynthesisInput(ssml=chunk)
            else:
                input_text = texttospeech.SynthesisInput(text=chunk)

            # Note: voice selection can be more complex, keeping it simple for now
            voice_params = {"language_code": self.language_code}
            if self.voice_name:
                voice_params["name"] = self.voice_name

            voice = texttospeech.VoiceSelectionParams(**voice_params)

            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3
            )

            try:
                response = self.client.synthesize_speech(
                    input=input_text, voice=voice, audio_config=audio_config
                )
                combined_audio += response.audio_content
                print(f"Synthesized chunk {i+1}/{len(text_chunks)}")
            except Exception as e:
                print(f"Error synthesizing chunk {i+1}: {e}")
                raise e

        with open(output_file, "wb") as out:
            out.write(combined_audio)
        
        print(f"Audio saved to {output_file}")
