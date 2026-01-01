print("KNOWLEDGE MODULE LOADED")
print("FILE:", __file__)
print("DIR:", dir())

from pathlib import Path
from app.auth import get_user_dir


def append_knowledge(user_id: str, text: str, source="user_notes.txt"):
    print("append_knowledge CALLED")

    user_dir = get_user_dir(user_id)
    docs_dir = user_dir / "documents"
    docs_dir.mkdir(exist_ok=True)

    file_path = docs_dir / source

    with open(file_path, "a", encoding="utf-8") as f:
        f.write("\n" + text.strip() + "\n")

    return file_path
