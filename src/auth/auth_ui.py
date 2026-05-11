"""
Auth UI Component
Renders login/signup forms with consistent Mizan styling.
"""

import streamlit as st
from src.auth.auth_manager import login, signup, ROLES

AUTH_CSS = """
<style>
.auth-container {
    max-width: 420px; margin: 4rem auto; padding: 2.5rem;
    background: #0D1017; border: 1px solid #1E2530;
    border-radius: 16px;
}
.auth-brand {
    text-align: center; margin-bottom: 2rem;
}
.auth-brand-icon {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, #C9A84C, #8B6914);
    border-radius: 14px; display: inline-flex;
    align-items: center; justify-content: center;
    font-size: 1.5rem; margin-bottom: 0.75rem;
}
.auth-brand h2 {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.8rem !important; font-weight: 600 !important;
    color: #C9A84C !important; margin: 0 !important;
}
.auth-brand p {
    font-size: 0.78rem !important; color: #3D4A5C !important;
    letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.25rem !important;
}
.auth-tab-bar {
    display: flex; gap: 0; margin-bottom: 1.75rem;
    background: #0A0C0F; border: 1px solid #1E2530; border-radius: 8px; overflow: hidden;
}
.auth-tab {
    flex: 1; padding: 0.6rem; text-align: center; font-size: 0.82rem;
    color: #3D4A5C; cursor: pointer; transition: all 0.2s;
}
.auth-tab.active { background: #1A2235; color: #C9A84C; }
.auth-error {
    background: #1A0808; border: 1px solid #3D0A0A; border-radius: 8px;
    padding: 0.6rem 0.9rem; font-size: 0.8rem; color: #CF6679; margin-bottom: 1rem;
}
.auth-success {
    background: #0C1F14; border: 1px solid #1A3828; border-radius: 8px;
    padding: 0.6rem 0.9rem; font-size: 0.8rem; color: #4CAF7D; margin-bottom: 1rem;
}
</style>
"""


def render_auth_page():
    """Render login/signup page. Returns True when authenticated."""
    st.markdown(AUTH_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="auth-container">
            <div class="auth-brand">
                <div class="auth-brand-icon">⚖️</div>
                <h2>Mizan</h2>
                <p>Pakistani Legal AI</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        tab = st.radio("", ["Sign In", "Create Account"],
                       horizontal=True, label_visibility="collapsed",
                       key="auth_tab")

        if tab == "Sign In":
            _render_login()
        else:
            _render_signup()

    return st.session_state.get("authenticated", False)


def _render_login():
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        submitted = st.form_submit_button("Sign In →", use_container_width=True)

    if submitted:
        if not username or not password:
            st.markdown('<div class="auth-error">Please enter username and password.</div>',
                        unsafe_allow_html=True)
        elif login(username, password):
            st.success(f"Welcome back, {username}!")
            st.rerun()
        else:
            st.markdown('<div class="auth-error">Invalid username or password.</div>',
                        unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-top:1.5rem;font-size:0.72rem;color:#3D4A5C">
        Demo accounts: <code style="color:#C9A84C">admin / admin123</code> &nbsp;·&nbsp;
        <code style="color:#C9A84C">lawyer1 / law12345</code>
    </div>
    """, unsafe_allow_html=True)


def _render_signup():
    role_options = {
        "🏠 Citizen — General Legal Help": "citizen",
        "⚖️ Lawyer — Professional Use": "lawyer",
        "📚 Student — Academic Research": "student",
    }

    with st.form("signup_form"):
        username = st.text_input("Username", placeholder="Choose a username (min 3 chars)")
        email = st.text_input("Email", placeholder="your@email.com")
        role_label = st.selectbox("I am a...", list(role_options.keys()))
        password = st.text_input("Password", type="password", placeholder="Min 6 characters")
        confirm = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
        submitted = st.form_submit_button("Create Account →", use_container_width=True)

    if submitted:
        role = role_options[role_label]
        result = signup(username, email, password, confirm, role)
        if result["success"]:
            st.markdown(f'<div class="auth-success">✓ {result["message"]} Please sign in.</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="auth-error">{result["message"]}</div>',
                        unsafe_allow_html=True)
