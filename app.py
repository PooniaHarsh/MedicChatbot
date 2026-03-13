from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from hospital_finder import find_nearby_hospitals, geocode_location
from triage import triage_symptoms


app = FastAPI(title="Healthcare Chatbot MVP", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    message: str = Field(..., description="User symptom description")
    location_text: Optional[str] = Field(default=None, description="City/area, e.g. 'Delhi' or 'Noida Sector 62'")
    lat: Optional[float] = None
    lon: Optional[float] = None


class HospitalItem(BaseModel):
    name: str
    address: str
    lat: str
    lon: str


class ChatResponse(BaseModel):
    disclaimer: str
    severity: str
    emergency: bool
    advice: str
    follow_up_questions: List[str]
    nearby_hospitals: List[HospitalItem]


DISCLAIMER = (
    "This bot gives general health guidance only and is not a medical diagnosis. "
    "For emergency symptoms, contact emergency services immediately."
)


@app.get("/")
def home() -> FileResponse:
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "healthcare-chatbot-mvp"}


@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    if not payload.message.strip():
        raise HTTPException(status_code=400, detail="message cannot be empty")

    triage_result = triage_symptoms(payload.message)

    hospitals: List[HospitalItem] = []
    lat, lon = payload.lat, payload.lon

    if lat is None or lon is None:
        if payload.location_text:
            geo = geocode_location(payload.location_text)
            if geo:
                lat, lon = geo

    if lat is not None and lon is not None:
        try:
            found = find_nearby_hospitals(lat=lat, lon=lon)
            hospitals = [HospitalItem(**h) for h in found]
        except Exception:
            hospitals = []

    if triage_result.emergency and not hospitals and (lat is None or lon is None):
        triage_result.advice += " Share your location to get nearby hospitals."

    return ChatResponse(
        disclaimer=DISCLAIMER,
        severity=triage_result.severity,
        emergency=triage_result.emergency,
        advice=triage_result.advice,
        follow_up_questions=triage_result.follow_up_questions,
        nearby_hospitals=hospitals,
    )
