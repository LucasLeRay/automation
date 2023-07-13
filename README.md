# Automation

Set of tools to automate my processes.

## How to setup?
Some tools imply that you are on a specific system (such as macOS), details are provided for each tool.

Some environment variables need to be provided (an option is to put them in `.env`):
```sh
OPENAI_API_KEY=...
OBSIDIAN_VAULT_NAME=...  # What is the vault where tools should save notes?
DEFAULT_TRANSCRIPT_SINCE=...  # From what date should the "transcript" tool search for voice recordings? (%Y-%m-%d)
```

## Transcript

Transcript recordings from Apple Voice Memos into Obsidian.
It assumes that memos were recorded in French.

```sh
python -m automation transcript
```

1. Fetch new recordings in iCloud
2. Transcript them (using OpenAI Whisper)
3. Enhance them (using OpenAI GPT)
4. Store them in Obsidian
