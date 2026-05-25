import sqlite3
import hashlib
import uuid
from datetime import datetime
from src.config import DB_PATH

# ── Schema ────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    username   TEXT UNIQUE NOT NULL,
    email      TEXT UNIQUE NOT NULL,
    password   TEXT NOT NULL,
    role       TEXT DEFAULT 'citizen',
    is_active  INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    last_login TEXT
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    session_id TEXT,
    role       TEXT,
    content    TEXT,
    mode       TEXT DEFAULT 'citizen',
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS documents (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    title      TEXT,
    doc_type   TEXT,
    content    TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS analyses (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    filename   TEXT,
    analysis   TEXT,
    risk_score REAL,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS strategies (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER,
    title      TEXT,
    situation  TEXT,
    strategy   TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
"""

DEMO_USERS = [
    ("admin",    "admin@mizan.ai",      "admin123",  "admin"),
    ("lawyer1",  "lawyer1@mizan.ai",    "law12345",  "lawyer"),
    ("student1", "student1@mizan.ai",   "stu12345",  "student"),
    ("citizen1", "citizen1@mizan.ai",   "cit12345",  "citizen"),
]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    # Seed demo users
    for username, email, password, role in DEMO_USERS:
        try:
            conn.execute(
                "INSERT OR IGNORE INTO users (username, email, password, role) VALUES (?,?,?,?)",
                (username, email, hash_password(password), role)
            )
        except Exception:
            pass
    conn.commit()
    conn.close()


# ── Auth ──────────────────────────────────────────────────────
def get_user_by_username(username: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username: str, email: str, password: str, role: str = "citizen"):
    conn = get_conn()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?,?,?,?)",
            (username, email, hash_password(password), role)
        )
        conn.commit()
        return {"success": True, "message": "Account created successfully"}
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return {"success": False, "message": "Username already taken"}
        return {"success": False, "message": "Email already registered"}
    finally:
        conn.close()


def verify_password(plain: str, hashed: str) -> bool:
    return hash_password(plain) == hashed


def update_last_login(user_id: int):
    conn = get_conn()
    conn.execute("UPDATE users SET last_login=? WHERE id=?", (datetime.now().isoformat(), user_id))
    conn.commit()
    conn.close()


# ── Messages ──────────────────────────────────────────────────
def save_message(user_id: int, session_id: str, role: str, content: str, mode: str = "citizen"):
    conn = get_conn()
    conn.execute(
        "INSERT INTO messages (user_id, session_id, role, content, mode) VALUES (?,?,?,?,?)",
        (user_id, session_id, role, content, mode)
    )
    conn.commit()
    conn.close()


def get_chat_sessions(user_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT session_id,
               MAX(created_at) as last_at,
               COUNT(*) as message_count,
               MAX(mode) as mode,
               (SELECT content FROM messages m2
                WHERE m2.session_id=m.session_id AND m2.role='user'
                ORDER BY m2.created_at LIMIT 1) as title
        FROM messages m WHERE user_id=?
        GROUP BY session_id ORDER BY last_at DESC
    """, (user_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_session_messages(user_id: int, session_id: str):
    conn = get_conn()
    rows = conn.execute(
        "SELECT * FROM messages WHERE user_id=? AND session_id=? ORDER BY created_at",
        (user_id, session_id)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_session(user_id: int, session_id: str):
    conn = get_conn()
    conn.execute("DELETE FROM messages WHERE user_id=? AND session_id=?", (user_id, session_id))
    conn.commit()
    conn.close()


# ── Documents ─────────────────────────────────────────────────
def save_document(user_id: int, title: str, doc_type: str, content: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO documents (user_id, title, doc_type, content) VALUES (?,?,?,?)",
        (user_id, title, doc_type, content)
    )
    conn.commit()
    conn.close()


def get_documents(user_id: int):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, doc_type, created_at FROM documents WHERE user_id=? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def delete_document(user_id: int, doc_id: int):
    conn = get_conn()
    conn.execute("DELETE FROM documents WHERE id=? AND user_id=?", (doc_id, user_id))
    conn.commit()
    conn.close()


# ── Strategies ────────────────────────────────────────────────
def save_strategy(user_id: int, title: str, situation: str, strategy: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO strategies (user_id, title, situation, strategy) VALUES (?,?,?,?)",
        (user_id, title[:100], situation, strategy)
    )
    conn.commit()
    conn.close()


def get_strategies(user_id: int):
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, title, situation, created_at FROM strategies WHERE user_id=? ORDER BY created_at DESC",
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ── Admin ─────────────────────────────────────────────────────
def get_all_users():
    conn = get_conn()
    rows = conn.execute("SELECT id,username,email,role,is_active,created_at,last_login FROM users ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def toggle_user_active(user_id: int):
    conn = get_conn()
    conn.execute("UPDATE users SET is_active = 1 - is_active WHERE id=?", (user_id,))
    conn.commit()
    conn.close()


def get_analytics():
    conn = get_conn()
    total_users     = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    total_messages  = conn.execute("SELECT COUNT(*) FROM messages").fetchone()[0]
    total_documents = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    total_strategies= conn.execute("SELECT COUNT(*) FROM strategies").fetchone()[0]
    users_by_role   = conn.execute("SELECT role, COUNT(*) as c FROM users GROUP BY role").fetchall()
    active_today    = conn.execute(
        "SELECT COUNT(DISTINCT user_id) FROM messages WHERE created_at >= date('now')"
    ).fetchone()[0]
    conn.close()
    return {
        "total_users":      total_users,
        "total_messages":   total_messages,
        "total_documents":  total_documents,
        "total_strategies": total_strategies,
        "users_by_role":    {r["role"]: r["c"] for r in users_by_role},
        "active_today":     active_today,
    }
