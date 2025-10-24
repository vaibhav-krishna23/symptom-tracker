"""Initialization or Placeholder File."""
# app/main.py
from fastapi import FastAPI
from app.db.session import engine, Base
from app.api.v1 import auth, sessions, dashboard

# Create tables (dev only)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Symptom Tracker API")

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(dashboard.router)
