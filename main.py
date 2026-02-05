
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from gemini_helper import analyze_voice  # your existing helper function

app = FastAPI()

# -------------------------------
# Replace this with your actual secret API key
API_KEY = AIzaSyBjfYeWVH80VKBeEoB6vhvCMuutYmZuHKo
# -------------------------------

# -------------------------------
# API Key verification dependency
# -------------------------------
async def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# -------------------------------
# Request model
# -------------------------------
class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str


# -------------------------------
# Voice detection endpoint
# -------------------------------
@app.post("/api/voice-detection")
async def detect_voice(req: VoiceRequest, request: Request):
    # Check API key
    await verify_api_key(request)

    # Extract data from request
    language = req.language
    audio_base64 = req.audioBase64

    # Call your existing voice detection function
    # It should return a dict like:
    # {"classification": "AI_GENERATED", "confidence": 0.91, "explanation": "..."}
    result = analyze_voice(language, audio_base64)

    # Return JSON response
    return {
        "status": "success",
        "language": language,
        "classification": result["classification"],
        "confidenceScore": result["confidence"],
        "explanation": result["explanation"]
    }


# -------------------------------
# Optional: Root health check
# -------------------------------
@app.get("/")
def root():
    return {"status": "API is running"}

