"""Initialization or Placeholder File."""
# streamlit_app/pages/_logger.py
import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from api_client import submit_session, book_appointment


def app():
    # Professional styling for logger
    st.markdown("""
    <style>
    .logger-header {
        text-align: center;
        color: #1f4e79;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .logger-subtitle {
        text-align: center;
        color: #5a6c7d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .section-header {
        color: #2d5aa0;
        font-weight: 600;
        border-left: 4px solid #4a90e2;
        padding-left: 1rem;
        margin: 1.5rem 0 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='logger-header'>🌡️ Symptom Logger</h1>", unsafe_allow_html=True)
    st.markdown("<p class='logger-subtitle'>How are you feeling today? Let's track your symptoms.</p>", unsafe_allow_html=True)
    
    if "token" not in st.session_state:
        st.warning("⚠️ Please login first")
        return
    
    # Initialize booking state
    if 'booking_choice' not in st.session_state:
        st.session_state.booking_choice = None
    if 'booking_result' not in st.session_state:
        st.session_state.booking_result = None
    if 'red_flag_session' not in st.session_state:
        st.session_state.red_flag_session = None
    
    # Check if we're in booking flow
    if st.session_state.red_flag_session and st.session_state.booking_choice is None:
        # Show red flag alert and booking options
        r = st.session_state.red_flag_session
        
        st.error("🚩 **RED FLAG ALERT - IMMEDIATE ATTENTION NEEDED**")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.warning(f"🔥 **Severity Score:** {r.get('severity', 0)}/10")
            st.info(f"🤖 **AI Analysis:** {r.get('ai_summary', '')}")
        with col2:
            st.markdown("🏥")
            st.markdown("**Urgent medical attention recommended**")
        
        st.markdown("---")
        st.markdown("### 📞 Your symptoms seem severe. Can we process an appointment with a doctor for you?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📅 ✅ YES - Book Emergency Appointment", type="primary", use_container_width=True):
                st.session_state.booking_choice = "yes"
                st.rerun()
                
        with col2:
            if st.button("❌ NO - Just Log Symptoms", use_container_width=True):
                st.session_state.booking_choice = "no"
                st.rerun()
    
    elif st.session_state.booking_choice == "yes":
        # Handle appointment booking
        if st.session_state.booking_result is None:
            with st.spinner("🔍 Finding available doctor in your area..."):
                booking_result = book_appointment(st.session_state["token"], st.session_state.red_flag_session["session_id"])
                st.session_state.booking_result = booking_result
            st.rerun()
        
        # Show booking result
        booking_result = st.session_state.booking_result
        if booking_result.get("error"):
            st.error(f"❌ **Booking Failed:** {booking_result['error']}")
            st.info("📞 Please call emergency services or visit nearest hospital")
        elif booking_result.get("appointment_id"):
            st.success("🎉 **APPOINTMENT SUCCESSFULLY BOOKED!**")
            st.markdown("### 📅 Appointment Details:")
            st.info(f"👨⚕️ **Doctor:** {booking_result.get('doctor_name', 'Unknown')}")
            st.info(f"🏥 **Clinic:** {booking_result.get('clinic', 'Unknown')}")
            st.info(f"📅 **Date:** {booking_result.get('appointment_date', 'Unknown')[:16]}")
            st.balloons()
            st.success("📧 Confirmation details will be sent to your email")
        else:
            st.warning(f"Unexpected response: {booking_result}")
        
        if st.button("🔄 Log New Symptoms"):
            st.session_state.booking_choice = None
            st.session_state.booking_result = None
            st.session_state.red_flag_session = None
            st.rerun()
    
    elif st.session_state.booking_choice == "no":
        # Handle no booking choice
        st.info("✅ **Symptoms logged with HIGH PRIORITY flag**")
        st.warning("📞 A healthcare professional will contact you within 2 hours for follow-up")
        st.error("⚠️ If symptoms worsen, please seek immediate medical attention")
        
        if st.button("🔄 Log New Symptoms"):
            st.session_state.booking_choice = None
            st.session_state.red_flag_session = None
            st.rerun()
    
    else:
        # Normal symptom logging interface
        # Mood Section
        st.markdown("<div class='section-header'>😊 How's Your Mood?</div>", unsafe_allow_html=True)
        mood_emojis = ["😭 Very Sad", "😔 Sad", "😐 Neutral", "😊 Happy", "😄 Very Happy"]
        mood = st.select_slider("Mood Level", options=range(1, 6), value=3, format_func=lambda x: mood_emojis[x-1], label_visibility="collapsed")
        
        st.markdown("<div class='section-header'>🤒 Select Your Symptoms</div>", unsafe_allow_html=True)
        symptoms_list = ["🤒 Fever", "🧠 Headache", "🤢 Nausea", "😴 Fatigue", "😵💫 Dizziness", "😴 Sleep issues", "🍽️ Appetite change", "❓ Other"]
        selected = st.multiselect("Symptoms", symptoms_list, placeholder="Choose symptoms you're experiencing", label_visibility="collapsed")
        
        # Symptom Intensity
        symptom_items = []
        if selected:
            st.markdown("<div class='section-header'>📊 Rate Symptom Intensity</div>", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, s in enumerate(selected):
                with cols[i % 2]:
                    clean_symptom = s.split(" ", 1)[1] if " " in s else s
                    intensity = st.slider(f"{s}", 0, 10, 5, key=s, help="0 = No symptoms, 10 = Severe")
                    symptom_items.append({"symptom": clean_symptom, "intensity": intensity, "notes": "", "photo_url": None})
        
        st.markdown("<div class='section-header'>📝 Describe Your Symptoms</div>", unsafe_allow_html=True)
        text = st.text_area("Description", placeholder="Tell us more about how you're feeling in your own words...", height=100, label_visibility="collapsed")
        
        if st.button("📝 Submit Symptoms", type="primary", use_container_width=True):
            if not symptom_items and not text:
                st.warning("⚠️ Please select symptoms or provide a description")
            else:
                payload = {"mood": mood, "symptoms": symptom_items, "free_text": text}
                
                with st.spinner("Analyzing your symptoms..."):
                    r = submit_session(st.session_state["token"], payload)
                
                if r.get("error"):
                    st.error(f"❌ Error: {r['error']}")
                elif r.get("red_flag"):
                    # Store session and trigger red flag flow
                    st.session_state.red_flag_session = r
                    st.rerun()
                else:
                    st.success("✅ **Thank you! Your symptoms have been logged successfully**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.info(f"📊 **Severity Score:** {r.get('severity', 0)}/10")
                    with col2:
                        st.info("📈 **Status:** Normal monitoring")
                    
                    if r.get('ai_summary'):
                        st.markdown("### 🤖 AI Health Summary:")
                        st.write(r['ai_summary'])
                    
                    st.success("📱 Continue monitoring your health. Log new symptoms anytime!")