# 24/7 AI Healthcare Chatbot (MVP)

This is a practical MVP chatbot backend that:
- Accepts symptom text
- Gives basic severity suggestions (low/medium/high)
- Flags possible serious cases for emergency action
- Finds nearby hospitals using OpenStreetMap (no API key needed)

## Important Safety Note
This is **not** a diagnosis tool. It gives general guidance only.
Always consult a qualified medical professional.

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run Project From VS Code
1. Open this folder in VS Code.

2. Select Python interpreter:
- `Ctrl + Shift + P` -> `Python: Select Interpreter` -> choose `.venv`.

3. Open VS Code terminal:
- `Terminal` -> `New Terminal`

4. Start server in VS Code terminal:
```bash
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

5. Open in browser:
- Bot app: `http://127.0.0.1:8000/`
- Health check: `http://127.0.0.1:8000/health`

6. Stop server:
- Press `Ctrl + C` in the terminal where server is running.

## Run (generic command)
```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

Keep this process running on a server/VPS/cloud to make it available 24/7.

## API
### Health check
`GET /health`

### Web chatbot UI
`GET /`

### Chat endpoint
`POST /chat`

Sample request:
```json
{
  "message": "I have chest pain and shortness of breath",
  "location_text": "Noida"
}
```

Sample response includes:
- `severity`
- `emergency`
- `advice`
- `follow_up_questions`
- `nearby_hospitals`

## Next upgrades
- WhatsApp/Telegram integration
- Persistent chat history (database)
- Appointment booking integration
- Medication reminders
- Clinically validated triage workflow
