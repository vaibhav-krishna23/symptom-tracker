import os

# Define the root directory for the project
PROJECT_ROOT = "symptom_tracker_project"

# List of all files and directories to create
structure = [
    # Top-level files
    (".env.example", "ENVIRONMENT=development\nSECRET_KEY=your_secure_secret"),
    ("requirements.txt", "fastapi==0.103.1\nuvicorn[standard]==0.23.2\nsqlalchemy==2.0.21\npydantic==2.4.2\nstreamlit==1.27.2\n"),
    ("README.md", "# Symptom Tracker Project\n\nThis project consists of a FastAPI backend and a Streamlit frontend for tracking and analyzing symptoms."),

    # App backend structure (with empty content for all Python files)
    "app/",
    "app/__init__.py",
    "app/main.py",
    "app/crud.py",

    # app/api/v1/
    "app/api/",
    "app/api/__init__.py",
    "app/api/v1/",
    "app/api/v1/__init__.py",
    "app/api/v1/auth.py",
    "app/api/v1/sessions.py",
    "app/api/v1/dashboard.py",

    # app/core/
    "app/core/",
    "app/core/__init__.py",
    "app/core/config.py",
    "app/core/security.py",

    # app/db/
    "app/db/",
    "app/db/__init__.py",
    "app/db/models.py",
    "app/db/session.py",

    # app/schemas/
    "app/schemas/",
    "app/schemas/__init__.py",
    "app/schemas/patient.py",
    "app/schemas/session.py",
    "app/schemas/appointment.py",

    # app/services/
    "app/services/",
    "app/services/__init__.py",
    "app/services/ai_processor.py",
    "app/services/appointment_scheduler.py",
    "app/services/email_service.py",

    # Streamlit frontend structure
    "streamlit_app/",
    "streamlit_app/__init__.py",
    "streamlit_app/app.py",
    "streamlit_app/api_client.py",
    "streamlit_app/pages/",
    "streamlit_app/pages/__init__.py",
    "streamlit_app/pages/_login.py",
    "streamlit_app/pages/_logger.py",
    "streamlit_app/pages/_dashboard.py",
]

def create_structure():
    """Creates all directories and files defined in the structure list."""
    # Ensure the root directory exists
    os.makedirs(PROJECT_ROOT, exist_ok=True)
    os.chdir(PROJECT_ROOT)

    print(f"Creating project structure in: ./{PROJECT_ROOT}/\n")

    for item in structure:
        content = ""
        # Check if the item is a tuple (file path, content)
        if isinstance(item, tuple):
            filepath, content = item
        # Otherwise, assume it's just the filepath/dirname
        else:
            filepath = item

        # Split path to handle nested directories
        dirname = os.path.dirname(filepath)

        # 1. Handle directories (including nested ones like 'app/api/v1')
        if not content and not "." in os.path.basename(filepath):
            os.makedirs(filepath, exist_ok=True)
            print(f"DIR: {filepath}/")
        
        # 2. Handle files
        else:
            # Ensure parent directories exist before creating the file
            if dirname:
                os.makedirs(dirname, exist_ok=True)

            # Add simple pass/import statement to Python files
            if filepath.endswith(".py"):
                content = content or '"""Initialization or Placeholder File."""\n'

            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"FILE: {filepath}")
            except Exception as e:
                print(f"Error creating {filepath}: {e}")

if __name__ == "__main__":
    create_structure()
    print("\n✅ Project structure created successfully!")
