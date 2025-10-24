"""Daily Symptom Tracker - Main Application"""
# streamlit_app/app.py
import streamlit as st
import components_login as _login
import components_logger as _logger
import components_dashboard as _dashboard

# Page configuration
st.set_page_config(
    page_title="Daily Symptom Tracker",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load custom CSS
def load_css():
    try:
        with open('style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass  # CSS file not found, continue without custom styling

load_css()

PAGES = {
    "Login": _login,
    "Symptom Logger": _logger,
    "Dashboard": _dashboard
}

# Professional sidebar styling
st.markdown("""
<style>
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #1f4e79 0%, #2d5aa0 100%);
}
.sidebar-title {
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
    text-align: center;
    padding: 1rem 0;
    border-bottom: 2px solid rgba(255,255,255,0.2);
    margin-bottom: 1rem;
}
.sidebar-tagline {
    color: #b8d4f0;
    font-size: 0.8rem;
    text-align: center;
    margin-bottom: 1.5rem;
    font-style: italic;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<div class='sidebar-title'>🏥 Daily Symptom Tracker</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-tagline'>by Value Health Inc.</div>", unsafe_allow_html=True)

# Check login status and control navigation
if "token" not in st.session_state:
    # Not logged in - only show login page
    _login.app()
else:
    # Logged in - show navigation and default to Symptom Logger
    if "current_page" not in st.session_state:
        st.session_state["current_page"] = "Symptom Logger"
    
    st.sidebar.markdown("### 📋 Navigation")
    page = st.sidebar.radio("Go to", ["🌡️ Symptom Logger", "📊 Dashboard"], index=0 if st.session_state["current_page"] == "Symptom Logger" else 1, label_visibility="collapsed")
    
    # Clean page name for session state
    if "🌡️ Symptom Logger" in page:
        st.session_state["current_page"] = "Symptom Logger"
    else:
        st.session_state["current_page"] = "Dashboard"
    
    # User info and logout
    st.sidebar.markdown("---")
    st.sidebar.markdown("👤 **Logged In**")
    st.sidebar.markdown("🟢 Status: Active")
    st.sidebar.markdown("")
    
    if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    
    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("🏥 **Daily Symptom Tracker**")
    st.sidebar.markdown("*Your Health Monitoring Companion*")
    st.sidebar.markdown("**Value Health Inc.**")
    st.sidebar.markdown("Version 1.0.0")
    
    if st.session_state["current_page"] == "Symptom Logger":
        _logger.app()
    else:
        _dashboard.app()
