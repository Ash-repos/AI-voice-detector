import os
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from gemini_helper import analyze_voice

app = FastAPI()

# Use an environment variable for your app's internal API key
API_KEY = os.getenv("APP_API_KEY")

async def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if not API_KEY or key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
async def detect_voice(req: VoiceRequest, request: Request):
    await verify_api_key(request)
    
    language = req.language
    audio_base64 = req.audioBase64

    result = analyze_voice(language, audio_base64)

    return {
        "status": "success",
        "language": language,
        "classification": result["classification"],
        "confidenceScore": result["confidenceScore"],
        "explanation": result["explanation"]
    }

@app.get("/")
def root():
    return {"status": "API is running"}
