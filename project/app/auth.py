from pathlib import Path

BASE_USER_DIR = Path("data/users")


def get_user_dir(user_id: str) -> Path:
    """
    Returns the base directory for a given user.
    Creates it if it does not exist.
    """
    user_dir = BASE_USER_DIR / user_id
    user_dir.mkdir(parents=True, exist_ok=True)
    return user_dir
