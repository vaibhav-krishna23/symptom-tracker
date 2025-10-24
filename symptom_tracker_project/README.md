# Symptom Tracker Project - Starter

## Setup

1. Copy `.env.example` to `.env` and fill values (DATABASE_URL, REDIS_URL, FERNET_KEY, GEMINI_API_KEY).
   - Generate Fernet key:
     ```py
     from cryptography.fernet import Fernet
     print(Fernet.generate_key().decode())
     ```

2. Create virtual environment and install:
   ```bash
   python -m venv venv
   source venv/bin/activate     # Windows: venv\Scripts\activate
   pip install -r requirements.txt
