"""Initialization or Placeholder File."""
# streamlit_app/pages/_login.py
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import login, register


def app():
    # Custom CSS for professional styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        color: #1f4e79;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .tagline {
        text-align: center;
        color: #5a6c7d;
        font-size: 1.2rem;
        font-weight: 400;
        margin-bottom: 0.3rem;
    }
    .company {
        text-align: center;
        color: #8fa8b8;
        font-size: 0.9rem;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .form-container {
        background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #d1e7dd;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='main-header'>🏥 Daily Symptom Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='tagline'>Your Health Monitoring Companion</p>", unsafe_allow_html=True)
    st.markdown("<p class='company'>by Value Health Inc.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='form-container'>", unsafe_allow_html=True)
        choice = st.selectbox("Choose an option:", ["Login", "Register"], index=0)
        if choice == "Register":
            st.markdown("### 📝 Create New Account")
            with st.form("reg", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    name = st.text_input("👤 Full Name", placeholder="Enter your full name")
                    email = st.text_input("📧 Email", placeholder="your.email@example.com")
                    city = st.text_input("🏢 City", placeholder="Your city")
                with col2:
                    password = st.text_input("🔒 Password", type="password", placeholder="Create a strong password")
                    secret_key = st.text_input("🔑 Secret Key", type="password", placeholder="Personal secret key")
                
                if st.form_submit_button("🚀 Create Account", use_container_width=True, type="primary"):
                    if all([name, email, password, secret_key, city]):
                        r = register({"full_name": name, "email": email, "password": password, "secret_key": secret_key, "city": city})
                        if r.get("error"):
                            st.error(f"❌ {r['error']}")
                        else:
                            st.success("✅ Account created successfully! Please login.")
                    else:
                        st.warning("⚠️ Please fill in all fields")
        else:
            st.markdown("### 👋 Welcome Back")
            with st.form("login"):
                email = st.text_input("📧 Email", placeholder="your.email@example.com")
                password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
                secret_key = st.text_input("🔑 Secret Key", type="password", placeholder="Enter your secret key")
                
                if st.form_submit_button("🔐 Sign In", use_container_width=True, type="primary"):
                    if all([email, password, secret_key]):
                        with st.spinner("Logging in..."):
                            r = login({"email": email, "password": password, "secret_key": secret_key})
                        if r.get("access_token"):
                            st.session_state["token"] = r["access_token"]
                            st.session_state["current_page"] = "Symptom Logger"
                            st.success("✅ Logged in successfully! Redirecting...")
                            st.rerun()
                        else:
                            st.error("❌ Login failed. Please check your credentials.")
                    else:
                        st.warning("⚠️ Please fill in all fields")
        st.markdown("</div>", unsafe_allow_html=True)
