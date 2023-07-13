import logging
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Tuple

from automation.config import config
from automation.directories import directories
from automation.tools.ai import generate_response, speech_to_text
from automation.tools.prompts import NOTE_TO_TITLE, TEXT_TO_NOTE

logger = logging.getLogger(__name__)

try:
    CONNECTION = sqlite3.connect(config.store_path)
except sqlite3.OperationalError:
    logger.error("Database was not found. Try to run 'make setup-store'.")
    sys.exit(1)
CURSOR = CONNECTION.cursor()


@dataclass
class Recording:
    date: datetime.date
    id_: str
    path: Path


def main():
    _create_table_if_not_exist()

    logger.info("Getting latest recording date...")
    latest_recording_date = _get_latest_recording_date()
    logger.info(f"Getting recordings since {latest_recording_date}")

    logger.info("Getting new recordings...")
    new_recordings = _get_new_recordings(latest_recording_date)

    # Recordings are not transcripted asynchronously, so I can cancel easily.
    for recording in new_recordings:
        logger.info(f"Transcripting recording from {recording.date}...")
        transcript = _transcript_audio(recording.path)

        logger.info("Enhancing text...")
        note, title = _transcript_to_note(transcript, date=recording.date)

        logger.info(f"Saving note '{title}' in Obsidian...")
        saved_path = _write_note(note, title)
        logger.info(f"Note saved in {saved_path}!")

        logger.debug("Update store with recording...")
        _update_store_from_recording(recording)


def _create_table_if_not_exist():
    CURSOR.execute("CREATE TABLE IF NOT EXISTS transcript(id, date)")


def _get_latest_recording_date() -> datetime.date:
    query = "SELECT MAX(date) FROM transcript"
    latest_date = CURSOR.execute(query).fetchone()[0]

    if not latest_date:
        return config.transcript.default_since.date()
    return datetime.strptime(latest_date, "%Y-%m-%d").date()


def _get_new_recordings(last_update: datetime) -> Iterable[Recording]:
    all_recordings = map(lambda recording: Recording(
        date=datetime.strptime(recording.stem.split(" ")[0], "%Y%m%d").date(),
        id_=recording.stem.split(" ")[1],
        path=recording,
    ), directories.voice_memos.glob("*.m4a"))

    return sorted(
        filter(lambda recording: recording.date > last_update, all_recordings),
        key=lambda recording: recording.date
    )


def _transcript_audio(audio_path: Path) -> str:
    with open(audio_path, "rb") as audio_file:
        return speech_to_text(audio_file)


def _transcript_to_note(
    transcript: str, *, date: datetime.date
) -> Tuple[str, str]:
    note = (
        generate_response(TEXT_TO_NOTE.format(text=transcript))
        + f"\n\n(Transcripted with {config.openai.whisper_version} "
        + f"& enhanced by {config.openai.gpt_version})"
    )
    title = (
        generate_response(NOTE_TO_TITLE.format(note=note)) + f" ({date})"
    )

    return note, title


def _write_note(note: str, title: str) -> Path:
    path = config.obsidian_vault_path / "Recordings" / f"{title}.md"
    with open(path, "w") as f:
        f.write(note)
    return path


def _update_store_from_recording(recording: Recording):
    CURSOR.execute(
        "INSERT INTO transcript VALUES "
        f"('{recording.id_}', '{recording.date}')"
    )
    CONNECTION.commit()


if __name__ == "__main__":
    main()
