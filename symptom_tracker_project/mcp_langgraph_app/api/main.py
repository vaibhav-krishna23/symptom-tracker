"""FastAPI application integrating MCP + LangGraph"""
from fastapi import FastAPI, Depends, HTTPException, Header, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from pathlib import Path
import uuid
import shutil
import sys
import os

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.db.session import get_db, engine, Base
from app.db import models
from app import crud
from app.schemas.patient import PatientCreate, PatientLogin, Token
from jose import jwt
from datetime import datetime, timedelta
from mcp_langgraph_app.config.settings import settings
from mcp_langgraph_app.langgraph_agent.fastmcp_client import FastMCPClient
from mcp_langgraph_app.langgraph_agent.agent_fixed import SymptomTrackerAgent
from mcp_langgraph_app.api.appointment_booking import router as appointment_router
from mcp_langgraph_app.api.fastmcp_routes import router as fastmcp_router

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title="Symptom Tracker with MCP + LangGraph",
    description="AI-Powered Healthcare Monitoring with MCP and LangGraph",
    version="2.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(appointment_router)
app.include_router(fastmcp_router)

# Create uploads directory and mount static files
UPLOAD_DIR = Path("uploads/symptom_photos")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# FastMCP server script path
FASTMCP_SERVER_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "mcp_server",
    "fastmcp_server.py"
)


# Pydantic Models
class SymptomInput(BaseModel):
    symptom: str
    intensity: int
    notes: Optional[str] = None
    photo_url: Optional[str] = None


class SymptomSubmission(BaseModel):
    symptoms: List[SymptomInput]
    mood: int
    free_text: str


class AppointmentBooking(BaseModel):
    session_id: str


# Helper Functions
def get_patient_id_from_token(authorization: str = Header(None)) -> str:
    """Extract patient ID from JWT token."""
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authentication scheme")
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        patient_id = payload.get("sub")
        if not patient_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return patient_id
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


# Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Symptom Tracker API with MCP + LangGraph",
        "version": "2.0.0",
        "features": ["MCP Tools", "LangGraph Workflow", "AI Analysis", "Appointment Booking"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "mcp_server": f"{settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}",
        "database": "connected",
        "timestamp": datetime.utcnow().isoformat()
    }


# Authentication Routes
@app.post("/api/v1/auth/register", response_model=dict)
def register(payload: PatientCreate, db: Session = Depends(get_db)):
    """Register a new patient."""
    existing = crud.get_patient_by_email(db, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    patient = crud.create_patient(
        db,
        payload.full_name,
        payload.email,
        payload.password,
        payload.secret_key,
        payload.city
    )
    
    return {
        "patient_id": str(patient.patient_id),
        "message": "Registration successful"
    }


@app.post("/api/v1/auth/login", response_model=Token)
def login(payload: PatientLogin, db: Session = Depends(get_db)):
    """Login and get access token."""
    user = crud.verify_patient_credentials(db, payload.email, payload.password, payload.secret_key)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": str(user.patient_id)})
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Symptom Tracking Routes (MCP + LangGraph)
@app.post("/api/v2/symptoms/submit")
async def submit_symptoms_langgraph(
    payload: SymptomSubmission,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """
    Submit symptoms using LangGraph workflow with FastMCP tools.
    This is the new FastMCP + LangGraph powered endpoint.
    """
    try:
        patient_id = get_patient_id_from_token(authorization)
        
        # Convert symptoms to dict format
        symptoms_list = [
            {
                "symptom": s.symptom,
                "intensity": s.intensity,
                "notes": s.notes,
                "photo_url": s.photo_url
            }
            for s in payload.symptoms
        ]
        
        # Process through LangGraph agent with FastMCP
        async with FastMCPClient(FASTMCP_SERVER_SCRIPT) as mcp_client:
            agent = SymptomTrackerAgent(mcp_client)
            result = await agent.process_symptoms(
                patient_id=patient_id,
                symptoms=symptoms_list,
                mood=payload.mood,
                free_text=payload.free_text
            )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Processing failed"))
        
        return {
            "success": True,
            "session_id": result["session_id"],
            "ai_analysis": result["ai_analysis"],
            "severity_check": result["severity_check"],
            "appointment_info": result.get("appointment_info", {}),
            "workflow_messages": result["messages"]
        }
    except Exception as e:
        import traceback
        print("\n" + "="*60)
        print("ERROR IN /api/v2/symptoms/submit:")
        print("="*60)
        traceback.print_exc()
        print("="*60 + "\n")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/api/v2/symptoms/history")
async def get_symptom_history(
    authorization: str = Header(None),
    limit: int = 10
):
    """Get patient symptom history using FastMCP tool."""
    patient_id = get_patient_id_from_token(authorization)
    
    async with FastMCPClient(FASTMCP_SERVER_SCRIPT) as mcp_client:
        result = await mcp_client.call_tool(
            "get_patient_history",
            patient_id=patient_id,
            limit=limit
        )
    
    if not result.get("success"):
        raise HTTPException(status_code=404, detail=result.get("error", "History not found"))
    
    return result


# Dashboard Routes
@app.get("/api/v1/dashboard/sessions")
def get_patient_sessions(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get all patient sessions."""
    patient_id = get_patient_id_from_token(authorization)
    
    sessions = crud.get_sessions_by_patient(db, patient_id)
    
    return {
        "sessions": [
            {
                "session_id": str(s.session_id),
                "start_time": s.start_time.isoformat() if s.start_time else None,
                "severity_score": float(s.severity_score) if s.severity_score else 0,
                "red_flag": s.red_flag,
                "ai_summary": s.ai_summary
            }
            for s in sessions
        ]
    }


@app.get("/api/v1/dashboard/session/{session_id}/details")
def get_session_details(
    session_id: str,
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get detailed session information including chat logs."""
    patient_id = get_patient_id_from_token(authorization)
    
    # Verify session belongs to patient
    session = db.query(models.Session).filter(
        models.Session.session_id == session_id,
        models.Session.patient_id == patient_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get symptoms
    symptoms = db.query(models.SymptomEntry).filter(
        models.SymptomEntry.session_id == session_id
    ).all()
    
    # Get chat logs
    chat_logs = crud.get_chat_logs(db, session_id)
    
    from app.core import security
    
    return {
        "session": {
            "session_id": str(session.session_id),
            "start_time": session.start_time.isoformat() if session.start_time else None,
            "severity_score": float(session.severity_score) if session.severity_score else 0,
            "red_flag": session.red_flag,
            "ai_summary": session.ai_summary
        },
        "symptoms": [
            {
                "symptom": s.symptom,
                "intensity": s.intensity,
                "notes": security.decrypt_bytes(s.notes) if s.notes else None,
                "photo_url": s.photo_url
            }
            for s in symptoms
        ],
        "chat_logs": [
            {
                "sender": log.sender,
                "message": security.decrypt_bytes(log.message) if log.message else "",
                "timestamp": log.timestamp.isoformat() if log.timestamp else None
            }
            for log in chat_logs
        ]
    }


@app.get("/api/v1/dashboard/insights")
def get_dashboard_insights(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
):
    """Get comprehensive dashboard insights."""
    try:
        from sqlalchemy import desc
        from datetime import datetime, timedelta, timezone
        from collections import defaultdict
        
        patient_id = get_patient_id_from_token(authorization)
        sessions = db.query(models.Session).filter(
            models.Session.patient_id == patient_id
        ).order_by(desc(models.Session.start_time)).all()
        
        if not sessions:
            return {"total_sessions": 0, "total_symptoms": 0, "avg_severity": 0, "red_flag_count": 0, "weekly_trend": [], "monthly_overview": {}, "symptom_patterns": {}, "top_symptoms": {}}
        
        symptoms = db.query(models.SymptomEntry).join(models.Session).filter(models.Session.patient_id == patient_id).all()
        appointments = db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()
        
        # Current week daily trend
        now = datetime.now(timezone.utc)
        week_start = now - timedelta(days=now.weekday())
        daily_data = {}
        for i in range(7):
            day = week_start + timedelta(days=i)
            daily_data[day.strftime("%Y-%m-%d")] = {"day": day.strftime("%a"), "severity": 0, "count": 0}
        
        for s in sessions:
            if s.start_time:
                try:
                    st = s.start_time if s.start_time.tzinfo else s.start_time.replace(tzinfo=timezone.utc)
                    if st >= week_start:
                        day_key = st.strftime("%Y-%m-%d")
                        if day_key in daily_data:
                            daily_data[day_key]["count"] += 1
                            daily_data[day_key]["severity"] += float(s.severity_score or 0)
                except:
                    pass
        
        weekly_trend = [{"day": v["day"], "avg_severity": round(v["severity"] / v["count"], 1) if v["count"] > 0 else 0} for k, v in sorted(daily_data.items())]
        
        # Severity distribution
        severity_dist = {"Low (0-3)": 0, "Moderate (4-6)": 0, "High (7-10)": 0}
        for s in sessions:
            sev = float(s.severity_score or 0)
            if sev <= 3:
                severity_dist["Low (0-3)"] += 1
            elif sev <= 6:
                severity_dist["Moderate (4-6)"] += 1
            else:
                severity_dist["High (7-10)"] += 1
        
        # Monthly overview
        try:
            current_month = now.strftime("%Y-%m")
            month_sessions = [s for s in sessions if s.start_time and s.start_time.strftime("%Y-%m") == current_month]
            day_names = [s.start_time.strftime("%A") for s in month_sessions if s.start_time]
            most_active = max(set(day_names), key=day_names.count) if day_names else "N/A"
        except:
            month_sessions = []
            most_active = "N/A"
        
        monthly_overview = {
            "month": now.strftime("%B %Y"),
            "total_sessions": len(month_sessions),
            "avg_severity": round(sum(float(s.severity_score or 0) for s in month_sessions) / len(month_sessions), 1) if month_sessions else 0,
            "red_flags": sum(1 for s in month_sessions if s.red_flag),
            "most_active_day": most_active
        }
        
        # Symptom patterns
        symptom_by_time = defaultdict(lambda: {"morning": 0, "afternoon": 0, "evening": 0, "night": 0})
        for symptom in symptoms:
            try:
                dt = symptom.date if hasattr(symptom, 'date') and symptom.date else None
                if dt:
                    hour = dt.hour
                    time_of_day = "morning" if 6 <= hour < 12 else "afternoon" if 12 <= hour < 18 else "evening" if 18 <= hour < 22 else "night"
                    symptom_by_time[symptom.symptom][time_of_day] += 1
            except:
                pass
        
        # Top symptoms
        symptom_counts = {}
        for s in symptoms:
            symptom_counts[s.symptom] = symptom_counts.get(s.symptom, 0) + 1
        top_symptoms = dict(sorted(symptom_counts.items(), key=lambda x: x[1], reverse=True)[:5]) if symptom_counts else {}
        
        return {
            "total_sessions": len(sessions),
            "total_symptoms": len(symptoms),
            "avg_severity": round(sum(float(s.severity_score or 0) for s in sessions) / len(sessions), 1),
            "red_flag_count": sum(1 for s in sessions if s.red_flag),
            "appointments_count": len(appointments),
            "weekly_trend": weekly_trend,
            "monthly_overview": monthly_overview,
            "severity_distribution": severity_dist,
            "top_symptoms": top_symptoms,
            "avg_mood": round(sum(s.mood for s in symptoms if hasattr(s, 'mood') and s.mood) / len([s for s in symptoms if hasattr(s, 'mood') and s.mood]), 1) if any(hasattr(s, 'mood') and s.mood for s in symptoms) else 0
        }
    except Exception as e:
        import traceback
        print("\n" + "="*60)
        print("ERROR IN /api/v1/dashboard/insights:")
        print("="*60)
        traceback.print_exc()
        print("="*60 + "\n")
        raise HTTPException(status_code=500, detail=f"Dashboard insights error: {str(e)}")


# MCP Tools Info
@app.get("/api/v2/mcp/tools")
async def list_mcp_tools():
    """List available FastMCP tools."""
    async with FastMCPClient(FASTMCP_SERVER_SCRIPT) as mcp_client:
        tools = await mcp_client.list_tools()
    return {"tools": [{"name": t.name, "description": t.description} for t in tools]}


# Doctor Management (Admin)
@app.post("/api/v1/admin/doctors")
def create_doctor(
    full_name: str,
    specialization: str,
    clinic_name: str,
    city: str,
    contact_email: str,
    contact_number: str = "",
    db: Session = Depends(get_db)
):
    """Create a new doctor (admin endpoint)."""
    doctor = crud.create_doctor(
        db,
        full_name=full_name,
        specialization=specialization,
        clinic_name=clinic_name,
        city=city,
        contact_email=contact_email
    )
    
    return {
        "doctor_id": str(doctor.doctor_id),
        "message": "Doctor created successfully"
    }


@app.get("/api/v1/admin/doctors")
def list_doctors(db: Session = Depends(get_db)):
    """List all doctors."""
    doctors = db.query(models.Doctor).all()
    
    return {
        "doctors": [
            {
                "doctor_id": str(d.doctor_id),
                "full_name": d.full_name,
                "specialization": d.specialization,
                "clinic_name": d.clinic_name,
                "city": d.city,
                "contact_email": d.contact_email
            }
            for d in doctors
        ]
    }


# Photo Upload
@app.post("/api/v1/upload/symptom-photo")
async def upload_symptom_photo(
    file: UploadFile = File(...),
    authorization: str = Header(None)
):
    """Upload symptom photo"""
    # Validate file type
    if file.content_type not in ["image/jpeg", "image/jpg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Only image files allowed")
    
    # Validate file size (max 5MB)
    contents = await file.read()
    if len(contents) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File must be less than 5MB")
    
    # Generate unique filename
    file_ext = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    file_path = UPLOAD_DIR / unique_filename
    
    # Save file
    with file_path.open("wb") as buffer:
        buffer.write(contents)
    
    return {
        "success": True,
        "photo_url": f"/uploads/symptom_photos/{unique_filename}",
        "filename": unique_filename
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
