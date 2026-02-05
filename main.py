from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from gemini_helper import analyze_voice

app = FastAPI()
API_KEY = "YOUR_SECRET_API_KEY"

class VoiceRequest(BaseModel):
    language: str
    audioFormat: str
    audioBase64: str

@app.post("/api/voice-detection")
def detect_voice(req: VoiceRequest, x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    if req.language not in ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]:
        raise HTTPException(status_code=400, detail="Unsupported language")
    if req.audioFormat.lower() != "mp3":
        raise HTTPException(status_code=400, detail="Audio must be MP3")

    try:
        result = analyze_voice(req.language, req.audioBase64)
        return {
            "status": "success",
            "language": req.language,
            **result
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}
