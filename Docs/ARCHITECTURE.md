# 🏗️ Architecture - System Design

## Overview

This project follows a clean, modular architecture designed for clarity and maintainability.

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT                                │
│     (Hackathon Tester / cURL / Postman / Your App)          │
└─────────────────────────┬───────────────────────────────────┘
                          │ HTTP POST
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                     FastAPI Server                           │
│  ┌───────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Authentication│  │  Validation  │  │ Error Handling   │  │
│  │  (API Key)    │  │ (Language,   │  │ (HTTP Exceptions)│  │
│  │               │  │  Format,     │  │                  │  │
│  │               │  │  Size)       │  │                  │  │
│  └───────┬───────┘  └──────┬───────┘  └──────────────────┘  │
│          │                 │                                 │
│          └────────┬────────┘                                 │
│                   ▼                                          │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                  Audio Processor                         ││
│  │  ┌─────────────────┐    ┌──────────────────────────┐    ││
│  │  │ Feature         │    │ Classification Engine    │    ││
│  │  │ Extraction      │───▶│ (Rule-Based Scoring)     │    ││
│  │  │ (librosa)       │    │                          │    ││
│  │  └─────────────────┘    └──────────────────────────┘    ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
                    JSON Response
```

---

## File Structure

```
AI_Voice_Detection/
├── main.py                 # FastAPI application (entry point)
├── audio_processor.py      # ML logic (feature extraction + classification)
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container configuration for Hugging Face
├── .env                    # Environment variables (API key)
├── .gitignore              # Files to exclude from git
│
├── Docs/                   # Documentation
│   ├── PROJECT_OVERVIEW.md
│   ├── HOW_IT_WORKS.md
│   ├── API_GUIDE.md
│   ├── AUDIO_FEATURES.md
│   └── ARCHITECTURE.md     # (this file)
│
├── test_sample/            # Sample audio files for testing
│   └── sample voice 1.mp3
│
└── (Helper scripts)
    ├── generate_base64.py  # Convert audio to Base64
    ├── verify_sample.py    # Test the API with sample
    └── keep_alive.py       # Keep Hugging Face Space alive
```

---

## Component Details

### 1. main.py - The API Layer

**Purpose:** Handle HTTP requests, validate inputs, route to processing.

**Key Components:**
- `FastAPI()` - The web framework
- `CORS Middleware` - Allow cross-origin requests
- `@app.post("/api/voice-detection")` - Main endpoint
- `@app.get("/health")` - Health check for monitoring

**Flow:**
```
Request → Auth Check → Input Validation → Process → Response
```

### 2. audio_processor.py - The Brain

**Purpose:** Extract features and classify voices.

**Key Functions:**
- `extract_audio_features()` - Uses librosa to get audio characteristics
- `classify_voice()` - Applies rules to determine AI vs Human
- `process_voice()` - Main entry point that combines both

**Decision Logic:**
```python
if ai_score > human_score:
    return "AI_GENERATED"
else:
    return "HUMAN"
```

### 3. Dockerfile - The Container

**Purpose:** Package the app for cloud deployment.

**Key Layers:**
```dockerfile
FROM python:3.12-slim
RUN apt-get install libsndfile1 ffmpeg  # Audio processing deps
COPY main.py audio_processor.py ...
CMD uvicorn main:app --host 0.0.0.0 --port 7860
```

---

## Request Lifecycle

### Happy Path

```
1. Client sends POST /api/voice-detection
   ├── Headers: x-api-key, Content-Type
   └── Body: {language, audioFormat, audioBase64}

2. main.py receives request
   ├── Validates API key → ✓ or 401
   ├── Validates language → ✓ or 400
   ├── Validates format → ✓ or 400
   └── Decodes Base64 → ✓ or 400

3. audio_processor.py processes
   ├── librosa loads audio
   ├── Extracts 10+ features
   ├── Scores against rules
   └── Returns classification

4. main.py returns JSON
   └── {status, language, classification, confidenceScore, explanation}
```

### Error Path

```
1. Invalid API key → 401 Unauthorized
2. Invalid input → 400 Bad Request
3. Processing error → 500 with caught exception
4. Unhandled error → 500 "Internal server error"
```

---

## Security Model

```
┌────────────────────────────────────────┐
│              Internet                   │
└─────────────────┬──────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│         API Key Validation              │
│  x-api-key header == API_KEY env var    │
│                                         │
│  ✗ No key → 401                         │
│  ✗ Wrong key → 401                      │
│  ✓ Valid key → Continue                 │
└─────────────────┬───────────────────────┘
                  │
                  ▼
           [Protected Endpoints]
```

**Key Points:**
- API key stored in environment variable (not in code)
- `.env` file is in `.gitignore` (never pushed to git)
- Hugging Face uses "Secrets" for secure storage

---

## Scaling Considerations

### Current Setup (Hackathon)
- Single Hugging Face Space
- ~2-5 second response time
- Handles ~10 concurrent requests

### If This Were Production
- Load balancer with multiple instances
- Redis cache for repeated requests
- Background queue for heavy processing
- Dedicated ML model instead of heuristics

---

## Technology Choices

| Choice | Why |
|--------|-----|
| **FastAPI** | Modern, fast, auto-generates docs |
| **librosa** | Industry-standard for audio analysis |
| **Hugging Face** | Free hosting with 48hr uptime |
| **Docker** | Consistent environments everywhere |
| **Rule-based ML** | Fast to implement, interpretable |

---

## Future Improvements

1. **Train a Real ML Model** - Use neural networks on labeled data
2. **Support More Formats** - WAV, FLAC, OGG
3. **Batch Processing** - Analyze multiple files at once
4. **Caching** - Store results for identical audio
5. **Webhooks** - Long-running analysis with callbacks

---

This architecture was designed to be **simple, clear, and functional** within hackathon constraints while remaining extensible for future development.
