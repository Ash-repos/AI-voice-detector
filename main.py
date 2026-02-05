from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

# Replace with your actual API key
API_KEY = "AIzaSyBjfYeWVH80VKBeEoB6vhvCMuutYmZuHKo"

# Dependency to check the key
async def verify_api_key(request: Request):
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
