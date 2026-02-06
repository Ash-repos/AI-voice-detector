import base64
import tempfile
import numpy as np
import librosa
import os
from google.genai import Client
from pydub import AudioSegment

# Fetch the API key from environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
client = Client(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-1.5-flash" # Updated to a valid model name

def extract_audio_features(audio_bytes: bytes):
    """Extract numeric features from MP3 audio."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp.flush()
        
        y, sr = librosa.load(tmp.name, sr=None)
        mfccs = np.mean(librosa.feature.mfcc(y=y, sr=sr), axis=1)
        pitch = np.mean(librosa.yin(y, fmin=75, fmax=600))
        energy = np.mean(librosa.feature.rms(y=y))
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        features_summary = (
            f"MFCCs mean: {mfccs.tolist()[:5]}, "
            f"Pitch: {pitch:.2f}, "
            f"Energy: {energy:.4f}, "
            f"Tempo: {tempo:.2f}"
        )
        
        return features_summary

def analyze_voice(language: str, audio_base64: str):
    audio_bytes = base64.b64decode(audio_base64)
    features_summary = extract_audio_features(audio_bytes)

    prompt = (
        f"You are an AI assistant that classifies voice recordings as HUMAN or AI_GENERATED.\n"
        f"Language: {language}\n"
        f"Audio features: {features_summary}\n"
        f"Provide a JSON output with fields: classification (HUMAN/AI_GENERATED), "
        f"confidenceScore (0.0-1.0), explanation."
    )

    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)

    try:
        # Improved parsing for JSON response
        import json
        text = response.text.replace('```json', '').replace('```', '').strip()
        result = json.loads(text)
        if not all(k in result for k in ["classification", "confidenceScore", "explanation"]):
            raise ValueError("Invalid format")
    except Exception:
        result = {
            "classification": "UNKNOWN",
            "confidenceScore": 0.0,
            "explanation": response.text
        }

    return result
