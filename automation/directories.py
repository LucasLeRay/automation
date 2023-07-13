from pathlib import Path
from types import SimpleNamespace

__all__ = ["directories"]

directories = SimpleNamespace()
directories.root = Path(__file__).parents[1]
directories.store = directories.root / "store"

# The following directories assume that the user works on a macOS environment.
directories.user_library = Path().home() / "Library"
directories.voice_memos = (
    directories.user_library
    / "Application Support" / "com.apple.voicememos" / "Recordings"
)
directories.obsidian = (
    directories.user_library
    / "Mobile Documents" / "iCloud~md~obsidian" / "Documents"
)
