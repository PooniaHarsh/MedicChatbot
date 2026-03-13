from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class TriageResult:
    severity: str
    advice: str
    follow_up_questions: List[str]
    emergency: bool


# Simple keyword-based triage for MVP use only.
# In production, replace with medically validated rules and clinician review.
SEVERE_KEYWORDS = {
    "chest pain",
    "difficulty breathing",
    "shortness of breath",
    "fainting",
    "seizure",
    "stroke",
    "paralysis",
    "severe bleeding",
    "blood vomiting",
    "suicidal",
    "unconscious",
}

MODERATE_KEYWORDS = {
    "fever",
    "high fever",
    "persistent cough",
    "vomiting",
    "diarrhea",
    "abdominal pain",
    "migraine",
    "rash",
    "infection",
}

MILD_KEYWORDS = {
    "cold",
    "runny nose",
    "sore throat",
    "mild headache",
    "tired",
    "fatigue",
    "body ache",
    "sneezing",
}


def triage_symptoms(user_text: str) -> TriageResult:
    text = user_text.lower().strip()

    severe_hits = [k for k in SEVERE_KEYWORDS if k in text]
    moderate_hits = [k for k in MODERATE_KEYWORDS if k in text]
    mild_hits = [k for k in MILD_KEYWORDS if k in text]

    if severe_hits:
        return TriageResult(
            severity="high",
            emergency=True,
            advice=(
                "This may be serious based on your symptoms. "
                "Please seek emergency care now or call your local emergency number immediately."
            ),
            follow_up_questions=[
                "How long have you had these symptoms?",
                "Are symptoms getting worse right now?",
                "Are you alone, or can someone help you reach emergency care?",
            ],
        )

    if moderate_hits:
        return TriageResult(
            severity="medium",
            emergency=False,
            advice=(
                "Your symptoms may need same-day medical attention. "
                "If symptoms worsen (breathing issues, severe pain, confusion), go to emergency care."
            ),
            follow_up_questions=[
                "What is your age?",
                "Do you have any chronic conditions (asthma, diabetes, heart disease)?",
                "Have you taken any medicine already?",
            ],
        )

    if mild_hits or text:
        return TriageResult(
            severity="low",
            emergency=False,
            advice=(
                "Symptoms appear mild at the moment. Rest, hydrate, and monitor for 24-48 hours. "
                "If you get worse, contact a doctor."
            ),
            follow_up_questions=[
                "Do you also have fever above 101F (38.3C)?",
                "Are symptoms improving, stable, or worsening?",
            ],
        )

    return TriageResult(
        severity="unknown",
        emergency=False,
        advice="I could not understand the symptoms clearly. Please describe them in more detail.",
        follow_up_questions=[
            "What symptoms are you having?",
            "When did they start?",
        ],
    )
