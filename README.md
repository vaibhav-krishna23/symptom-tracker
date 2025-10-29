# 🏥 Symptom Tracker v2.0 - MCP + LangGraph

AI-powered healthcare monitoring with **real Model Context Protocol (MCP)** and **LangGraph workflow orchestration**.

**New Architecture**: FastMCP + LangGraph + Google Gemini AI

## 🌟 Features

- 🔐 **Secure Authentication**: JWT-based user authentication with encrypted secret keys
- 📝 **Symptom Logging**: Interactive symptom tracking with intensity ratings and mood monitoring
- 🤖 **AI Analysis**: Google Gemini 2.5 Flash powered symptom analysis and severity scoring
- 🚩 **Red Flag Detection**: Automatic detection of severe symptoms requiring immediate attention
- 📅 **Smart Appointment Booking**: Automated doctor matching and appointment scheduling
- 📧 **Email Notifications**: Real-time email confirmations to both patients and doctors
- 📊 **Health Dashboard**: Comprehensive view of symptom history and session tracking
- 🏥 **Doctor Management**: Complete doctor database with specializations and availability

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database (Railway hosted)
- **SQLAlchemy**: Python SQL toolkit and ORM
- **Redis**: In-memory data structure store for caching (Railway hosted)
- **Pydantic**: Data validation using Python type annotations

### Frontend
- **Streamlit**: Interactive web application framework
- **Custom CSS**: Professional healthcare-themed UI design

### AI & Services
- **Google Gemini 2.5 Flash**: Advanced AI for symptom analysis
- **Gmail SMTP**: Email notification system
- **JWT**: Secure token-based authentication
- **Cryptography**: Fernet encryption for sensitive data

### Infrastructure
- **Railway**: Cloud database hosting
- **Git**: Version control

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- SQLite (included) or PostgreSQL
- Gmail account with app password
- Google Gemini API key

### Installation

```bash
# Clone repository
git clone https://github.com/vaibhav-krishna23/symptom-tracker.git
cd symptom-tracker/symptom_tracker_project

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# Install dependencies
cd mcp_langgraph_app
pip install -r requirements.txt

# Configure .env file
cp .env.example .env
# Edit .env with your credentials

# Add sample doctor
python add_doctor.py
```

### Run Application (3 Terminals)

**Terminal 1: MCP Server**
```bash
cd mcp_langgraph_app
python run_mcp_server.py
```

**Terminal 2: FastAPI Backend**
```bash
cd mcp_langgraph_app
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 3: Streamlit Frontend**
```bash
cd mcp_langgraph_app
streamlit run streamlit_app/app_v2.py
```

**Access**: http://localhost:8501

## 📋 Usage

### For Patients
1. **Register/Login**: Create account with email and secure secret key
2. **Log Symptoms**: Select symptoms, rate intensity, and describe feelings
3. **AI Analysis**: Get instant AI-powered health assessment
4. **Emergency Care**: Automatic red flag detection for severe symptoms
5. **Book Appointments**: One-click emergency appointment booking
6. **Track History**: View complete symptom and appointment history

### For Healthcare Providers
- Receive instant email notifications for emergency appointments
- Access patient symptom summaries and AI analysis
- Manage appointment schedules and patient communications

## 🏗️ Project Structure

```
symptom_tracker_project/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Configuration and security
│   ├── db/              # Database models and session
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic services
│   └── main.py          # FastAPI application
├── streamlit_app/
│   ├── components_*.py  # UI components
│   ├── api_client.py    # API communication
│   └── app.py           # Main Streamlit app
└── .env                 # Environment configuration
```

## 🔄 Workflow

### Normal Symptom Logging (Severity < 8)
1. User logs symptoms and mood
2. AI analyzes and generates summary
3. Data stored in database
4. User receives confirmation

### Red Flag Alert (Severity ≥ 8)
1. User logs severe symptoms
2. AI detects high severity/red flag
3. **Immediate Alert**: Red flag warning displayed
4. **Appointment Options**: "Book Emergency Appointment" or "Just Log Symptoms"
5. **If Booking**: 
   - System finds available doctor in user's city
   - Creates appointment in database
   - Sends emails to both patient and doctor
   - Displays confirmation with appointment details

## 🔒 Security Features

- **Encrypted Storage**: Sensitive data encrypted using Fernet
- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: SHA256 password hashing
- **Input Validation**: Comprehensive data validation
- **Environment Variables**: Secure configuration management

## 📊 Database Schema

- **Patients**: User accounts and profiles
- **Doctors**: Healthcare provider information
- **Sessions**: Symptom logging sessions
- **Symptoms**: Individual symptom entries
- **Appointments**: Scheduled medical appointments
- **Chat Logs**: AI conversation history
- **Notifications**: Email and communication logs

## 🤖 AI Integration

The system uses Google Gemini 2.5 Flash for:
- Symptom severity scoring (0-10 scale)
- Medical summary generation
- Red flag detection for emergency cases
- Treatment recommendations

## 📧 Email System

Automated email notifications include:
- **Patient Confirmations**: Appointment details and symptom summaries
- **Doctor Alerts**: New emergency patient notifications
- **Medical Summaries**: Complete symptom analysis and chat logs

## 🏷️ Version

**v2.0.0** - MCP + LangGraph Architecture

**Key Changes**:
- ✅ Real FastMCP with 7 tools
- ✅ LangGraph 8-node workflow
- ✅ SQLite support for local development
- ✅ Simplified architecture

## 👥 Contributing

This is a healthcare application. Please ensure all contributions maintain:
- Patient data privacy and security
- Medical accuracy and reliability
- Compliance with healthcare regulations

## 📄 License

Developed by Value Health AI Inc.

## 🆘 Support

For technical support or medical emergencies:
- Technical Issues: Create GitHub issue
- Medical Emergencies: Contact emergency services immediately

---

**⚠️ Medical Disclaimer**: This application is for symptom tracking and monitoring purposes only. It does not replace professional medical advice, diagnosis, or treatment. Always consult healthcare professionals for medical concerns.