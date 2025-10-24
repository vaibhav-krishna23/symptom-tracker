"""Initialization or Placeholder File."""
# streamlit_app/api_client.py
import requests
import os

BASE = os.getenv("API_BASE", "http://localhost:8000")

def register(data):
    try:
        response = requests.post(f"{BASE}/api/v1/auth/register", json=data)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def login(data):
    try:
        response = requests.post(f"{BASE}/api/v1/auth/login", json=data)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def submit_session(token, payload):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE}/api/v1/sessions/submit", json=payload, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}

def get_sessions(token):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE}/api/v1/dashboard/sessions", headers=headers)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return []

def get_logs(token, session_id):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE}/api/v1/dashboard/logs/{session_id}", headers=headers)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        return []

def book_appointment(token, session_id):
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE}/api/v1/sessions/book-appointment", 
                               json={"session_id": session_id}, headers=headers)
        return response.json() if response.status_code == 200 else {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
