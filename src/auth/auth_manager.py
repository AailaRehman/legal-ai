"""
Authentication Manager
Handles login, signup, session state, and role-based access.
"""

import uuid
from typing import Dict, Optional
import streamlit as st
from pathlib import Path
import sys

_project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_project_root))

from src.database.db_manager import authenticate_user, create_user, init_db

ROLES = {
    "citizen":  {"label": "Citizen",  "icon": "🏠", "color": "#4CAF7D"},
    "lawyer":   {"label": "Lawyer",   "icon": "⚖️", "color": "#C9A84C"},
    "student":  {"label": "Student",  "icon": "📚", "color": "#7A8ACF"},
    "admin":    {"label": "Admin",    "icon": "🛡️", "color": "#CF6679"},
}

ROLE_MODE_MAP = {
    "citizen": "Citizen",
    "lawyer":  "Lawyer",
    "student": "Student",
    "admin":   "Lawyer",
}


def init_auth():
    """Initialize auth session state."""
    init_db()
    defaults = {
        "authenticated": False,
        "user": None,
        "session_id": None,
        "auth_page": "login",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def login(username: str, password: str) -> bool:
    user = authenticate_user(username, password)
    if user:
        st.session_state.authenticated = True
        st.session_state.user = user
        st.session_state.session_id = str(uuid.uuid4())[:8]
        # Auto-set mode based on role
        st.session_state.mode = ROLE_MODE_MAP.get(user["role"], "Citizen")
        return True
    return False


def logout():
    for key in ["authenticated", "user", "session_id", "messages",
                "rag_chain", "vectorstore", "kb_loaded"]:
        st.session_state.pop(key, None)
    st.session_state.authenticated = False
    st.session_state.user = None


def signup(username: str, email: str, password: str,
           confirm: str, role: str = "citizen") -> Dict:
    if not username or not email or not password:
        return {"success": False, "message": "All fields are required."}
    if len(username) < 3:
        return {"success": False, "message": "Username must be at least 3 characters."}
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}
    if password != confirm:
        return {"success": False, "message": "Passwords do not match."}
    if "@" not in email:
        return {"success": False, "message": "Invalid email address."}
    return create_user(username, email, password, role)


def is_admin() -> bool:
    return (st.session_state.get("authenticated") and
            st.session_state.get("user", {}).get("role") == "admin")


def require_auth() -> bool:
    """Returns True if user is authenticated, shows login if not."""
    return st.session_state.get("authenticated", False)


def get_current_user() -> dict:
    return st.session_state.get("user", {})


def get_role_info(role: str) -> dict:
    return ROLES.get(role, ROLES["citizen"])


