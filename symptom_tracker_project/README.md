# 🏥 Symptom Tracker - MCP + LangGraph Healthcare System

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green.svg)](https://fastapi.tiangolo.com/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-orange.svg)](https://github.com/langchain-ai/langgraph)
[![FastMCP](https://img.shields.io/badge/FastMCP-Official-purple.svg)](https://github.com/jlowin/fastmcp)

AI-powered healthcare monitoring with **real MCP (Model Context Protocol)** and **LangGraph workflow orchestration**.

## 🌟 Features

- 🔧 **Real MCP**: Official FastMCP with stdio transport (7 tools)
- 🤖 **LangGraph**: 8-node stateful workflow with conditional routing
- 🧠 **AI Analysis**: Google Gemini 2.5 Flash symptom severity scoring
- 🏥 **Smart Doctor Matching**: AI-powered specialist selection
- 📅 **Auto Appointments**: Emergency appointment booking with email notifications
- 🔐 **Secure**: JWT auth + Fernet encryption
- 🎨 **Modern UI**: Dark-themed Streamlit interface

---

## 📁 Project Structure

```
symptom_tracker_project/
│
├── app/                          # 🔧 SHARED CORE MODULES (Used by v2)
│   ├── api/v1/                   # v1 API endpoints (auth, dashboard)
│   ├── core/                     # Security, encryption, config
│   ├── db/                       # 📊 Database models & session
│   │   ├── models.py            # SQLAlchemy models (Patient, Doctor, etc.)
│   │   └── session.py           # Database connection
│   ├── schemas/                  # Pydantic validation schemas
│   ├── services/                 # Business logic (legacy)
│   └── crud.py                   # 🔄 Database CRUD operations
│
└── mcp_langgraph_app/           # 🚀 V2.0 APPLICATION (FastMCP)
    ├── api/
    │   ├── main.py              # FastAPI v2 backend with FastMCP
    │   ├── appointment_booking.py  # Manual appointment endpoint
    │   └── fastmcp_routes.py    # FastMCP-specific routes
    │
    ├── config/
    │   └── settings.py          # Centralized configuration
    │
    ├── langgraph_agent/         # 🧠 LANGGRAPH WORKFLOW
    │   ├── agent_fixed.py       # 8-node workflow with routing
    │   └── fastmcp_client.py    # FastMCP client (stdio transport)
    │
    ├── mcp_server/              # 🛠️ FASTMCP SERVER (Official MCP)
    │   └── fastmcp_server.py    # 7 tools with @mcp.tool() decorators
    │
    ├── streamlit_app/           # 🎨 FRONTEND UI
    │   └── app_v2.py            # Dark theme Streamlit interface
    │
    ├── .env.example             # Environment template
    ├── requirements.txt         # Python dependencies
    ├── README.md                # Detailed documentation
    ├── ARCHITECTURE.md          # Architecture diagrams
    ├── CHANGELOG.md             # Version history
    └── COMMIT_GUIDE.md          # Git commit guide
```

---

## 🔗 How Folders Are Interconnected

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (app_v2.py)                 │
│                  Dark Theme Healthcare Interface             │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP REST API
┌────────────────────────────▼────────────────────────────────┐
│              FASTAPI BACKEND (main.py)                       │
│         • v2 endpoints (/api/v2/symptoms/submit)            │
│         • v1 auth endpoints (backward compatible)           │
│         • Appointment booking endpoint                      │
└────────────────────────────┬────────────────────────────────┘
                             │ Calls
┌────────────────────────────▼────────────────────────────────┐
│          LANGGRAPH AGENT (agent_fixed.py)                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  8 Nodes: analyze → check_severity → find_doctor    │  │
│  │           → save_session → create_appointment        │  │
│  │           → send_emails → complete                   │  │
│  │  Conditional Routing: emergency vs normal paths     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP Calls
┌────────────────────────────▼────────────────────────────────┐
│      FASTMCP SERVER (fastmcp_server.py - Embedded)          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  7 FastMCP Tools (@mcp.tool() decorators):          │  │
│  │  1. analyze_symptoms_with_ai (Gemini AI)            │  │
│  │  2. check_severity_threshold                         │  │
│  │  3. find_available_doctor (LLM-powered)             │  │
│  │  4. save_session_to_database                         │  │
│  │  5. create_appointment                               │  │
│  │  6. send_appointment_emails                          │  │
│  │  7. get_patient_history                              │  │
│  │                                                       │  │
│  │  Protocol: Official MCP with stdio transport        │  │
│  │  Returns: JSON strings (MCP compliant)              │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │ Uses
┌────────────────────────────▼────────────────────────────────┐
│              SHARED CORE (app/ folder)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • app/db/models.py - Database models               │  │
│  │  • app/db/session.py - DB connection                │  │
│  │  • app/crud.py - CRUD operations                    │  │
│  │  • app/core/security.py - Encryption                │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL    │
                    │   (Railway)     │
                    └─────────────────┘
```

---

## 🎯 Why the `app/` Folder Exists

The `app/` folder contains **SHARED CORE MODULES** that are used by the entire v2 application:

### ✅ Used by v2 Components:

| Module | Used By | Purpose |
|--------|---------|---------|
| `app/db/models.py` | MCP Server, LangGraph Agent | Database models (Patient, Doctor, Session, Appointment) |
| `app/db/session.py` | MCP Server, Appointment Booking | Database connection and session management |
| `app/crud.py` | MCP Server | CRUD operations for all database entities |
| `app/core/security.py` | MCP Server | Fernet encryption for sensitive data |
| `app/api/v1/auth.py` | FastAPI v2 Backend | Authentication endpoints (login/register) |

**Without the `app/` folder, v2 would NOT work!** It's the foundation that v2 is built upon.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- SQLite (included) or PostgreSQL
- Gmail account with app password
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vaibhav-krishna23/Symptoms-Tracker-Advanced.git
   cd Symptoms-Tracker-Advanced
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   cd mcp_langgraph_app
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   # Copy example env file
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env  # or use any text editor
   ```

   Required variables:
   ```env
   # Database (SQLite for local dev)
   DATABASE_URL=sqlite:///./symptom_tracker.db
   
   # AI
   GEMINI_API_KEY=your_gemini_api_key
   
   # Email
   SMTP_USER=your_email@gmail.com
   SMTP_PASS=your_app_password
   
   # Security
   JWT_SECRET_KEY=your_secret_key
   FERNET_KEY=your_fernet_key
   ```

5. **Add sample doctor**
   ```bash
   python add_doctor.py
   ```

---

## 🏃 Running the Application

**3 Terminal Setup:**

### Terminal 1: MCP Server
```bash
cd mcp_langgraph_app
python run_mcp_server.py
```

### Terminal 2: FastAPI Backend
```bash
cd mcp_langgraph_app
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```
**API Docs:** `http://localhost:8000/docs`

### Terminal 3: Streamlit Frontend
```bash
cd mcp_langgraph_app
streamlit run streamlit_app/app_v2.py
```
**Frontend:** `http://localhost:8501`

---

## 📊 Workflow Diagram

```
User Submits Symptoms
         ↓
    [Streamlit UI]
         ↓
   [FastAPI Backend]
         ↓
  [LangGraph Agent]
         ↓
    ┌────────────┐
    │ Analyze    │ → AI analyzes symptoms
    │ Symptoms   │    (Gemini 2.5 Flash)
    └─────┬──────┘
          ↓
    ┌────────────┐
    │ Check      │ → Severity score 0-10
    │ Severity   │
    └─────┬──────┘
          ↓
    Is Emergency? (≥8)
    ├─ YES → Find Doctor (LLM matches specialist)
    │         ↓
    │    Save Session
    │         ↓
    │    User Confirms?
    │    ├─ YES → Create Appointment → Send Emails
    │    └─ NO  → Complete
    │
    └─ NO  → Save Session → Complete
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| **MCP** | FastMCP (Official Protocol) |
| **Frontend** | Streamlit (Dark Theme UI) |
| **Backend** | FastAPI (Async REST API) |
| **Workflow** | LangGraph (State Management) |
| **AI** | Google Gemini 2.5 Flash |
| **Database** | SQLite / PostgreSQL |
| **Auth** | JWT + Fernet Encryption |
| **Email** | Gmail SMTP |

---

## 📝 API Endpoints

### v2 Endpoints (LangGraph)
- `POST /api/v2/symptoms/submit` - Submit symptoms (LangGraph workflow)
- `POST /api/v1/sessions/book-appointment` - Manual appointment booking

### v1 Endpoints (Backward Compatible)
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/register` - User registration
- `GET /api/v1/dashboard/sessions` - Get user sessions

---

## 🐳 Docker Deployment

### Docker Images Available

**Docker Hub**: `vaibhav547/symptom-tracker-api:latest` and `vaibhav547/symptom-tracker-web:latest`

### Quick Start with Docker Compose

```bash
# Run with docker-compose
docker-compose up -d

# Access
# Frontend: http://localhost:8501
# API: http://localhost:8000
```

### Manual Docker Run

```bash
# API
docker run -p 8000:8000 --env-file .env vaibhav547/symptom-tracker-api:latest

# Web
docker run -p 8501:8501 -e API_BASE=http://localhost:8000 vaibhav547/symptom-tracker-web:latest
```

### Cloud Deployment (Render)

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed Render deployment guide.

**Quick Deploy**:
1. Push images to Docker Hub (already done)
2. Create API service on Render with image `vaibhav547/symptom-tracker-api:latest`
3. Create Web service on Render with image `vaibhav547/symptom-tracker-web:latest`
4. Set environment variables
5. Deploy!

---

## 🧪 Testing Emergency Workflow

1. Register with your city name
2. Log symptoms with intensity ≥ 8 (e.g., Chest Pain: 9)
3. Describe: "Severe chest pain for 30 minutes"
4. Watch LangGraph execute the emergency workflow!

---

## 🔒 Security Features

- ✅ JWT-based authentication
- ✅ Fernet encryption for sensitive data
- ✅ Password hashing (SHA256)
- ✅ Environment variable protection
- ✅ Input validation with Pydantic

---

## 📄 License

Developed by **Value Health AI Inc.**

---

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/vaibhav-krishna23/Symptoms-Tracker-Advanced/issues)
- **Medical Emergencies**: Contact emergency services immediately

---

## ⚠️ Medical Disclaimer

This application is for symptom tracking and monitoring purposes only. It does **NOT** replace professional medical advice, diagnosis, or treatment. Always consult healthcare professionals for medical concerns.

---

## 🎯 Testing Emergency Workflow

1. Register with your city name
2. Log symptoms with intensity ≥ 8 (e.g., Chest Pain: 9)
3. Describe: "Severe chest pain for 30 minutes"
4. Watch LangGraph execute the emergency workflow!

---

**Version**: 2.0.0  
**Made with ❤️ by Vaibhav Krishna**  
**Powered by**: FastMCP + LangGraph + Google Gemini AI
