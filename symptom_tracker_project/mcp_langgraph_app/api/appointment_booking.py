"""Separate appointment booking endpoint"""
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db import models
from app import crud
from datetime import datetime, timedelta
from mcp_langgraph_app.langgraph_agent.fastmcp_client import FastMCPClient
from mcp_langgraph_app.config.settings import settings
import os

router = APIRouter()

# FastMCP server script path
FASTMCP_SERVER_SCRIPT = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "mcp_server",
    "fastmcp_server.py"
)

def get_patient_id_from_token(authorization: str = Header(None)) -> str:
    from jose import jwt
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        scheme, token = authorization.split()
    except:
        raise HTTPException(status_code=401, detail="Invalid Authorization header")
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return payload.get("sub")

@router.post("/api/v1/sessions/book-appointment")
async def book_appointment_manual(request: dict, authorization: str = Header(None), db: Session = Depends(get_db)):
    """Manual appointment booking with user confirmation"""
    patient_id = get_patient_id_from_token(authorization)
    session_id = request.get("session_id")
    
    if not session_id:
        raise HTTPException(status_code=400, detail="Session ID required")
    
    # Get session and verify ownership
    session = db.query(models.Session).filter(
        models.Session.session_id == session_id,
        models.Session.patient_id == patient_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get patient info
    patient = crud.get_patient_by_id(db, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # Get symptoms to determine specialization
    symptoms = db.query(models.SymptomEntry).filter(
        models.SymptomEntry.session_id == session_id
    ).all()
    
    # Determine specialization based on symptoms
    specialization_map = {
        "chest pain": "Cardiologist",
        "heart": "Cardiologist", 
        "headache": "Neurologist",
        "dizziness": "Neurologist",
        "confusion": "Neurologist",
        "rash": "Dermatologist",
        "skin": "Dermatologist",
        "nausea": "Gastroenterologist",
        "vomiting": "Gastroenterologist",
        "abdominal pain": "Gastroenterologist",
        "joint pain": "Orthopedist",
        "back pain": "Orthopedist"
    }
    
    needed_specialization = "General Practitioner"
    for symptom in symptoms:
        symptom_name = symptom.symptom.lower()
        for key, spec in specialization_map.items():
            if key in symptom_name:
                needed_specialization = spec
                break
    
    # Use FastMCP for all tool calls
    async with FastMCPClient(FASTMCP_SERVER_SCRIPT) as mcp_client:
        # Find doctor using MCP tool with symptoms
        doctor_result = await mcp_client.call_tool(
            "find_available_doctor",
            city=patient.city,
            specialization=needed_specialization,
            urgency="emergency",
            symptoms=[{"symptom": s.symptom, "intensity": s.intensity} for s in symptoms]
        )
        
        if not doctor_result.get("success"):
            return {"error": "No available doctors found in your city"}
        
        # Create appointment using MCP tool
        appointment_result = await mcp_client.call_tool(
            "create_appointment",
            patient_id=patient_id,
            doctor_id=doctor_result["doctor_id"],
            session_id=session_id,
            appointment_type="emergency",
            notes=session.ai_summary
        )
        
        if not appointment_result.get("success"):
            return {"error": "Failed to create appointment"}
        
        # Send emails using MCP tool
        from app.core.security import decrypt_bytes
        logs = crud.get_chat_logs(db, session_id)
        chat_summary = ""
        for log in logs:
            if log.sender == "patient":
                chat_summary += f"Patient: {decrypt_bytes(log.message)}\n"
            elif log.sender == "bot":
                chat_summary += f"AI: {decrypt_bytes(log.message)}\n"
        
        if not chat_summary:
            chat_summary = session.ai_summary or "High severity symptoms requiring immediate attention"
        
        # Extract photo URLs from symptoms
        photo_urls = [s.photo_url for s in symptoms if s.photo_url]
        
        print(f"\nCalling send_appointment_emails MCP tool...")
        print(f"   Patient: {appointment_result['patient_email']}")
        print(f"   Doctor: {appointment_result['doctor_email']}")
        
        try:
            email_result = await mcp_client.call_tool(
                "send_appointment_emails",
                patient_email=appointment_result["patient_email"],
                patient_name=appointment_result["patient_name"],
                doctor_email=appointment_result["doctor_email"],
                doctor_name=appointment_result["doctor_name"],
                clinic_name=appointment_result["clinic_location"],
                appointment_date=appointment_result["appointment_date"],
                symptoms_summary=chat_summary,
                appointment_type="emergency",
                photo_urls=photo_urls
            )
            print(f"SUCCESS: Email tool returned: {email_result}")
        except Exception as e:
            print(f"ERROR: Email tool error: {e}")
            email_result = {"success": False, "error": str(e)}
    
    # Log email result for debugging
    print(f"\nEMAIL RESULT: {email_result}")
    
    return {
        "success": True,
        "doctor_name": appointment_result.get("doctor_name"),
        "clinic": appointment_result.get("clinic_location"),
        "appointment_date": appointment_result.get("appointment_date"),
        "emails_sent": email_result.get("success", False),
        "email_error": email_result.get("error") if not email_result.get("success") else None,
        "email_details": email_result.get("errors"),
        "message": f"Appointment scheduled with Dr. {appointment_result.get('doctor_name')} at {appointment_result.get('clinic_location')}"
    }