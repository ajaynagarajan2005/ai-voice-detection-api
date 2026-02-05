"""
AI Voice Detection API
Detects AI-generated vs Human voices across 5 languages
"""

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import base64
import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="Detects AI-generated vs Human voices across Tamil, English, Hindi, Malayalam, and Telugu",
    version="1.0.0"
)

# CORS configuration for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration
VALID_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
VALID_FORMATS = ["mp3"]  
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found in environment variables! Please set it in .env or your deployment settings.")
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB limit


# Request/Response Models
class VoiceRequest(BaseModel):
    """Request model for voice detection endpoint"""
    language: str = Field(..., description="Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)")
    audioFormat: str = Field(..., description="Format of the audio file (mp3)")
    audioBase64: str = Field(..., description="Base64 encoded audio data")


class VoiceResponse(BaseModel):
    """Success response model"""
    status: str = "success"
    language: str
    classification: str  # AI_GENERATED or HUMAN
    confidenceScore: float = Field(..., ge=0.0, le=1.0)
    explanation: str


class ErrorResponse(BaseModel):
    """Error response model"""
    status: str = "error"
    message: str


# Import audio processing module
from core.audio_processor import process_voice as process_audio


# API Endpoints
@app.api_route("/", methods=["GET", "HEAD"])
async def root():
    """Root endpoint - API info"""
    return {
        "message": "AI Voice Detection API",
        "version": "1.0.0",
        "endpoints": {
            "voice-detection": "/api/voice-detection",
            "health": "/health"
        }
    }


@app.api_route("/health", methods=["GET", "HEAD"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}


@app.post("/api/voice-detection", response_model=None)
async def detect_voice(
    request: VoiceRequest,
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
):
    """
    Detect if voice is AI-generated or Human.
    
    - **language**: One of Tamil, English, Hindi, Malayalam, Telugu
    - **audioFormat**: Audio format (mp3)
    - **audioBase64**: Base64 encoded audio data
    
    Returns classification (AI_GENERATED or HUMAN) with confidence score.
    """
    
    # 1. Validate API Key
    if not x_api_key or x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail={"status": "error", "message": "Invalid or missing API key"}
        )
    
    # 2. Validate language
    if request.language not in VALID_LANGUAGES:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Invalid language. Must be one of: {', '.join(VALID_LANGUAGES)}"
            }
        )
    
    # 3. Validate audio format
    if request.audioFormat.lower() not in VALID_FORMATS:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Invalid audio format. Must be only : {', '.join(VALID_FORMATS)}"
            }
        )
    
    # 4. Decode and validate Base64 audio
    try:
        audio_bytes = base64.b64decode(request.audioBase64)
    except Exception:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Invalid Base64 encoding for audio data"
            }
        )
    
    # 5. Check file size
    if len(audio_bytes) > MAX_FILE_SIZE:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": f"Audio file too large. Maximum size is {MAX_FILE_SIZE // (1024*1024)}MB"
            }
        )
    
    # 6. Check minimum file size (at least 1KB for valid audio)
    if len(audio_bytes) < 1024:
        return JSONResponse(
            status_code=400,
            content={
                "status": "error",
                "message": "Audio file too small. Please provide a valid audio file"
            }
        )
    
    # 7. Process audio and get classification
    try:
        result = process_audio(audio_bytes, request.language)
        return result
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": f"Error processing audio: {str(e)}"
            }
        )


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail if isinstance(exc.detail, dict) else {"status": "error", "message": str(exc.detail)}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
