import os
from datetime import datetime
from types import SimpleNamespace

from dotenv import load_dotenv

from automation.directories import directories

__all__ = ["config"]

ENV_PATH = directories.root / ".env"


class _Config:
    def __init__(self):
        if ENV_PATH.exists():
            load_dotenv(ENV_PATH)

        self.openai = SimpleNamespace(
            api_key=os.environ.get("OPEN_API_KEY", ""),
            whisper_version="whisper-1",
            gpt_version="gpt-3.5-turbo"
        )
        self.store_path = directories.store / "store.db"

        self.obsidian_vault_path = (
            directories.obsidian / os.environ.get("OBSIDIAN_VAULT_NAME", "")
        )

        default_transcript_since = datetime.strptime(
            os.environ.get("DEFAULT_TRANSCRIPT_SINCE", "1970-01-01"),
            "%Y-%m-%d"
        )
        self.transcript = SimpleNamespace(
            default_since=default_transcript_since
        )


config = _Config()
