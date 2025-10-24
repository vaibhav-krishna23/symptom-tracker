"""Initialization or Placeholder File."""
# streamlit_app/pages/_dashboard.py
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import get_sessions, get_logs



def app():
    # Professional styling for dashboard
    st.markdown("""
    <style>
    .dashboard-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .dashboard-subtitle {
        text-align: center;
        color: #5a6c7d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .session-card {
        background: linear-gradient(135deg, #f8fbff 0%, #e8f4f8 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4a90e2;
        margin: 0.5rem 0;
    }
    .severity-high { border-left-color: #dc3545 !important; }
    .severity-medium { border-left-color: #ffc107 !important; }
    .severity-low { border-left-color: #28a745 !important; }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='dashboard-header'>📊 Health Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='dashboard-subtitle'>Track your health journey and view your symptom history</p>", unsafe_allow_html=True)
    
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first")
        return
    
    rows = get_sessions(st.session_state["token"])
    if not rows:
        st.info("📈 No health sessions recorded yet. Start by logging your symptoms!")
        return
    
    st.markdown(f"<div style='color: #2d5aa0; font-weight: 600; font-size: 1.3rem; margin: 1.5rem 0 1rem 0;'>📅 Your Health Sessions ({len(rows)} total)</div>", unsafe_allow_html=True)
    
    for i, r in enumerate(rows):
        # Create severity badge
        severity = r.get('severity_score', 0)
        if severity >= 8:
            severity_badge = "🔴 High"
            severity_color = "#ff4444"
        elif severity >= 5:
            severity_badge = "🟡 Medium"
            severity_color = "#ffaa00"
        else:
            severity_badge = "🟢 Low"
            severity_color = "#00aa00"
        
        red_flag_icon = "🚩" if r.get('red_flag') else "✅"
        
        with st.expander(f"{red_flag_icon} Session #{i+1} | Severity: {severity_badge} ({severity}) | {r.get('created_at', 'Unknown date')[:10] if r.get('created_at') else 'Unknown date'}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown("**🤖 AI Summary:**")
                st.write(r.get("ai_summary", "No summary available"))
            with col2:
                if st.button("📜 View Chat Logs", key=str(r["session_id"]), use_container_width=True):
                    logs = get_logs(st.session_state["token"], r["session_id"])
                    if logs:
                        st.markdown("**Chat History:**")
                        for l in logs:
                            sender_icon = "👤" if l.get('sender') == 'patient' else "🤖"
                            st.markdown(f"{sender_icon} **{l.get('sender', 'Unknown').title()}:** {l.get('message', 'No message')}")
                    else:
                        st.info("No chat logs available for this session")
