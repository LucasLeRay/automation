from typing import IO

import openai

from automation.config import config

__all__ = ["speech_to_text", "generate_response"]


def speech_to_text(audio_file: IO) -> str:
    """Transcript audio from file into text."""
    return openai.Audio.transcribe(config.openai.whisper_version, audio_file)


def generate_response(prompt) -> str:
    """send prompt to GPT model and return the response."""
    return openai.ChatCompletion.create(
        model=config.openai.gpt_version,
        messages=[{"role": "user", "content": prompt}]
    )["choices"][0]["message"]["content"]
