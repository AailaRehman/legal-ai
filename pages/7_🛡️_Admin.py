"""
Page 7: Admin Panel
User management and analytics — admin role only.
"""

import sys
from pathlib import Path
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.auth.auth_manager import init_auth, require_auth, is_admin, get_current_user
from src.auth.auth_ui import render_auth_page
from src.database.db_manager import get_analytics, get_all_users

st.set_page_config(page_title="Admin — Mizan", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,600;1,400&family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400&display=swap');
html, body, .stApp { background: #0A0C0F !important; color: #E8E4DC !important; font-family: 'DM Sans', sans-serif !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2.5rem 3rem !important; max-width: 1200px !important; }

.page-eyebrow { font-size: 0.68rem; letter-spacing: 0.2em; text-transform: uppercase; color: #CF6679; margin-bottom: 0.5rem; }
.page-title { font-family: 'Cormorant Garamond', serif; font-size: 2.4rem; font-weight: 300; color: #E8E4DC; line-height: 1.1; margin-bottom: 0.4rem; }
.page-title em { font-style: italic; color: #CF6679; }

.stat-card { background: #0D1017; border: 1px solid #1E2530; border-radius: 10px; padding: 1.25rem; text-align: center; }
.stat-card-num { font-family: 'DM Mono', monospace; font-size: 2.2rem; color: #C9A84C; display: block; }
.stat-card-label { font-size: 0.7rem; color: #3D4A5C; text-transform: uppercase; letter-spacing: 0.1em; }

.user-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 0.75rem 1rem; border-bottom: 1px solid #0F1520; font-size: 0.83rem;
}
.user-row:hover { background: #0D1017; }
.role-badge {
    display: inline-block; border-radius: 20px; padding: 0.15rem 0.6rem;
    font-size: 0.68rem; font-weight: 500; letter-spacing: 0.05em;
}
.role-citizen  { background: #0C1F14; color: #4CAF7D; border: 1px solid #1A3828; }
.role-lawyer   { background: #1A1A08; color: #C9A84C; border: 1px solid #2A2A18; }
.role-student  { background: #0C0C18; color: #7A8ACF; border: 1px solid #1A1A2A; }
.role-admin    { background: #1A0808; color: #CF6679; border: 1px solid #3D0A0A; }

.divider { height: 1px; background: linear-gradient(90deg, transparent, #1E2530 30%, #1E2530 70%, transparent); margin: 1.5rem 0; }
</style>
""", unsafe_allow_html=True)

init_auth()

if not require_auth():
    render_auth_page()
    st.stop()

if not is_admin():
    st.error("🛡️ Admin access required. You don't have permission to view this page.")
    st.markdown(f'<div style="color:#3D4A5C;font-size:0.8rem;margin-top:0.5rem">Logged in as: {get_current_user().get("username")} ({get_current_user().get("role")})</div>', unsafe_allow_html=True)
    st.stop()

# ── Header ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-eyebrow">🛡️ &nbsp; Admin Panel · Phase 4</div>
<div class="page-title">System <em>Analytics</em></div>
""", unsafe_allow_html=True)

# ── Analytics ──────────────────────────────────────────────────────────────────
analytics = get_analytics()
users = get_all_users()

cols = st.columns(4)
for col, (num, label) in zip(cols, [
    (analytics["total_users"],    "Total Users"),
    (analytics["total_messages"], "Total Messages"),
    (analytics["total_documents"],"Saved Documents"),
    (analytics["total_analyses"], "Saved Analyses"),
]):
    with col:
        st.markdown(f"""
        <div class="stat-card">
            <span class="stat-card-num">{num}</span>
            <span class="stat-card-label">{label}</span>
        </div>""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.75rem;font-weight:600">All Users</p>', unsafe_allow_html=True)
    st.markdown('<div style="background:#0D1017;border:1px solid #1E2530;border-radius:10px;overflow:hidden">', unsafe_allow_html=True)

    # Header row
    st.markdown("""
    <div class="user-row" style="color:#3D4A5C;font-size:0.65rem;text-transform:uppercase;letter-spacing:0.1em">
        <span style="flex:2">Username</span>
        <span style="flex:3">Email</span>
        <span style="flex:1">Role</span>
        <span style="flex:2">Joined</span>
        <span style="flex:2">Last Login</span>
    </div>""", unsafe_allow_html=True)

    for u in users:
        role = u.get("role", "citizen")
        joined = u.get("created_at", "")[:10]
        last_login = u.get("last_login", "Never")
        if last_login and len(last_login) > 10:
            last_login = last_login[:10]

        st.markdown(f"""
        <div class="user-row">
            <span style="flex:2;color:#C8CDD8;font-weight:500">{u['username']}</span>
            <span style="flex:3;color:#5A6478">{u['email']}</span>
            <span style="flex:1"><span class="role-badge role-{role}">{role}</span></span>
            <span style="flex:2;color:#3D4A5C;font-family:'DM Mono',monospace;font-size:0.75rem">{joined}</span>
            <span style="flex:2;color:#3D4A5C;font-family:'DM Mono',monospace;font-size:0.75rem">{last_login or 'Never'}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin-bottom:0.75rem;font-weight:600">Mode Usage</p>', unsafe_allow_html=True)

    for mode_data in analytics.get("top_modes", []):
        mode = mode_data.get("mode", "Unknown")
        count = mode_data.get("count", 0)
        total = analytics["total_messages"] or 1
        pct = int(count / total * 100)
        color = {"Citizen": "#4CAF7D", "Lawyer": "#C9A84C", "Student": "#7A8ACF"}.get(mode, "#5A6478")
        st.markdown(f"""
        <div style="margin-bottom:0.75rem">
            <div style="display:flex;justify-content:space-between;font-size:0.8rem;margin-bottom:0.3rem">
                <span style="color:#C8CDD8">{mode}</span>
                <span style="color:{color};font-family:'DM Mono',monospace">{count} ({pct}%)</span>
            </div>
            <div style="background:#0D1017;border-radius:4px;height:4px">
                <div style="background:{color};width:{pct}%;height:4px;border-radius:4px"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<p style="font-size:0.68rem;letter-spacing:0.15em;text-transform:uppercase;color:#3D4A5C;margin:1.5rem 0 0.75rem;font-weight:600">Recent Signups</p>', unsafe_allow_html=True)
    for u in analytics.get("recent_users", []):
        role = u.get("role", "citizen")
        st.markdown(f"""
        <div style="padding:0.5rem 0;border-bottom:1px solid #0F1520;font-size:0.8rem">
            <span style="color:#C8CDD8">{u['username']}</span>
            <span class="role-badge role-{role}" style="float:right">{role}</span>
        </div>""", unsafe_allow_html=True)
