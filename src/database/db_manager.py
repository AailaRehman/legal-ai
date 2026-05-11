"""
Database Manager — SQLite
Handles: users, sessions, chat history, saved documents, saved strategies.
"""

import sqlite3
import hashlib
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any

_project_root = Path(__file__).resolve().parent.parent.parent
DB_PATH = str(_project_root / "data" / "mizan.db")


def get_connection() -> sqlite3.Connection:
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create all tables if they don't exist."""
    conn = get_connection()
    c = conn.cursor()

    # Users table
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT UNIQUE NOT NULL,
            email       TEXT UNIQUE NOT NULL,
            password    TEXT NOT NULL,
            role        TEXT DEFAULT 'citizen',
            created_at  TEXT DEFAULT (datetime('now')),
            last_login  TEXT
        )
    """)

    # Chat history table
    c.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            session_id  TEXT NOT NULL,
            role        TEXT NOT NULL,
            content     TEXT NOT NULL,
            mode        TEXT DEFAULT 'Citizen',
            page        TEXT DEFAULT 'main',
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Saved documents table
    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_documents (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title       TEXT NOT NULL,
            doc_type    TEXT NOT NULL,
            content     TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Saved analyses table
    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_analyses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            filename    TEXT NOT NULL,
            analysis    TEXT NOT NULL,
            risk_score  INTEGER,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Saved strategies table
    c.execute("""
        CREATE TABLE IF NOT EXISTS saved_strategies (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            title       TEXT NOT NULL,
            situation   TEXT NOT NULL,
            strategy    TEXT NOT NULL,
            created_at  TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


# ── Password hashing ────────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed


# ── User management ─────────────────────────────────────────────────────────────

def create_user(username: str, email: str, password: str, role: str = "citizen") -> Dict:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
            (username.strip(), email.strip().lower(), hash_password(password), role)
        )
        conn.commit()
        return {"success": True, "message": "Account created successfully!"}
    except sqlite3.IntegrityError as e:
        if "username" in str(e):
            return {"success": False, "message": "Username already taken."}
        elif "email" in str(e):
            return {"success": False, "message": "Email already registered."}
        return {"success": False, "message": "Registration failed."}
    finally:
        conn.close()


def authenticate_user(username: str, password: str) -> Optional[Dict]:
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE username = ?", (username.strip(),)
        ).fetchone()
        if row and verify_password(password, row["password"]):
            conn.execute(
                "UPDATE users SET last_login = datetime('now') WHERE id = ?", (row["id"],)
            )
            conn.commit()
            return dict(row)
        return None
    finally:
        conn.close()


def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = get_connection()
    try:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def get_all_users() -> List[Dict]:
    """Admin only."""
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT id, username, email, role, created_at, last_login FROM users ORDER BY created_at DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Chat history ────────────────────────────────────────────────────────────────

def save_message(user_id: int, session_id: str, role: str,
                 content: str, mode: str = "Citizen", page: str = "main"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO chat_history (user_id, session_id, role, content, mode, page) VALUES (?,?,?,?,?,?)",
            (user_id, session_id, role, content, mode, page)
        )
        conn.commit()
    finally:
        conn.close()


def get_chat_history(user_id: int, session_id: Optional[str] = None,
                     page: str = "main", limit: int = 50) -> List[Dict]:
    conn = get_connection()
    try:
        if session_id:
            rows = conn.execute(
                "SELECT * FROM chat_history WHERE user_id=? AND session_id=? AND page=? ORDER BY created_at LIMIT ?",
                (user_id, session_id, page, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM chat_history WHERE user_id=? AND page=? ORDER BY created_at DESC LIMIT ?",
                (user_id, page, limit)
            ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_user_sessions(user_id: int, page: str = "main") -> List[Dict]:
    """Get distinct chat sessions for a user."""
    conn = get_connection()
    try:
        rows = conn.execute("""
            SELECT session_id, page, mode,
                   MIN(created_at) as started_at,
                   COUNT(*) as message_count,
                   MAX(created_at) as last_message
            FROM chat_history
            WHERE user_id=? AND page=?
            GROUP BY session_id
            ORDER BY last_message DESC
            LIMIT 20
        """, (user_id, page)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_session(user_id: int, session_id: str):
    conn = get_connection()
    try:
        conn.execute(
            "DELETE FROM chat_history WHERE user_id=? AND session_id=?",
            (user_id, session_id)
        )
        conn.commit()
    finally:
        conn.close()


# ── Saved documents ─────────────────────────────────────────────────────────────

def save_document(user_id: int, title: str, doc_type: str, content: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO saved_documents (user_id, title, doc_type, content) VALUES (?,?,?,?)",
            (user_id, title, doc_type, content)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_saved_documents(user_id: int) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM saved_documents WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def delete_document(user_id: int, doc_id: int):
    conn = get_connection()
    try:
        conn.execute(
            "DELETE FROM saved_documents WHERE id=? AND user_id=?",
            (doc_id, user_id)
        )
        conn.commit()
    finally:
        conn.close()


# ── Saved analyses ──────────────────────────────────────────────────────────────

def save_analysis(user_id: int, filename: str, analysis: str, risk_score: int = 0) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO saved_analyses (user_id, filename, analysis, risk_score) VALUES (?,?,?,?)",
            (user_id, filename, analysis, risk_score)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_saved_analyses(user_id: int) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM saved_analyses WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Saved strategies ────────────────────────────────────────────────────────────

def save_strategy(user_id: int, title: str, situation: str, strategy: str) -> bool:
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO saved_strategies (user_id, title, situation, strategy) VALUES (?,?,?,?)",
            (user_id, title, situation, strategy)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_saved_strategies(user_id: int) -> List[Dict]:
    conn = get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM saved_strategies WHERE user_id=? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


# ── Analytics (admin) ────────────────────────────────────────────────────────────

def get_analytics() -> Dict:
    conn = get_connection()
    try:
        total_users = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        total_messages = conn.execute("SELECT COUNT(*) FROM chat_history").fetchone()[0]
        total_docs = conn.execute("SELECT COUNT(*) FROM saved_documents").fetchone()[0]
        total_analyses = conn.execute("SELECT COUNT(*) FROM saved_analyses").fetchone()[0]

        top_modes = conn.execute("""
            SELECT mode, COUNT(*) as count FROM chat_history
            GROUP BY mode ORDER BY count DESC
        """).fetchall()

        recent_users = conn.execute("""
            SELECT username, role, created_at FROM users
            ORDER BY created_at DESC LIMIT 5
        """).fetchall()

        return {
            "total_users": total_users,
            "total_messages": total_messages,
            "total_documents": total_docs,
            "total_analyses": total_analyses,
            "top_modes": [dict(r) for r in top_modes],
            "recent_users": [dict(r) for r in recent_users],
        }
    finally:
        conn.close()


# Initialize DB on import
init_db()
