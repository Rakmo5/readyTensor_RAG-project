import sqlite3
from pathlib import Path
from datetime import datetime, timezone

from project.app.auth import get_user_dir


def get_memory_db(user_id: str) -> sqlite3.Connection:
    """
    Returns a SQLite connection for the user's memory DB.
    Creates the DB and table if it does not exist.
    """
    user_dir = get_user_dir(user_id)
    db_path = user_dir / "chat.db"

    conn = sqlite3.connect(db_path)
    _initialize_db(conn)
    return conn


def _initialize_db(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()


def save_message(user_id: str, role: str, content: str):
    conn = get_memory_db(user_id)
    cursor = conn.cursor()

    query = """
    INSERT INTO messages (role, content, timestamp)
    VALUES (?, ?, ?)
    """

    cursor.execute(
        query,
        (role, content, datetime.now(timezone.utc).isoformat())
    )

    conn.commit()
    conn.close()


def load_recent_messages(user_id: str, limit: int = 10):
    conn = get_memory_db(user_id)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT role, content
        FROM messages
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()
    conn.close()

    return list(reversed(rows))
