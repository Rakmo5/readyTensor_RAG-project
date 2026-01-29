from pathlib import Path
from project.app.auth import get_user_dir

def append_knowledge(user_id: str, text: str, source="user_notes.txt"):
    """
    Safely appends a new note to the user's specific knowledge base file.
    """
    # 1. Get the base directory for the user
    user_dir = get_user_dir(user_id)
    
    # 2. Define and create the documents directory if it doesn't exist
    # Use parents=True and exist_ok=True for robust directory creation
    docs_dir = user_dir / "documents"
    docs_dir.mkdir(parents=True, exist_ok=True)

    file_path = docs_dir / source

    # 3. Append text using a context manager ('with' statement)
    # Explicitly set encoding to 'utf-8' to prevent issues on different OSs
    with open(file_path, "a", encoding="utf-8") as f:
        # Ensure the new entry starts on a fresh line
        f.write(f"\n{text.strip()}\n")

    return file_path