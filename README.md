---
title: AI Voice Detection
emoji: 🌍
colorFrom: gray
colorTo: pink
sdk: docker
pinned: false
---

# 🎤 AI Voice Detection API

> **Test whether your audio sample is AI-generated or human speech**

[![Hugging Face](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Tamizh019/AI_Voice_Detection)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)

---

## Our Team

- **Ajay**
- **Tamizharasan**
- **Varshini Sekar**
- **Faheem**

---

## 🚀 Live Demo

**API Endpoint:** `https://tamizh019-ai-voice-detection.hf.space/api/voice-detection`

### Test with cURL

We've provided sample Base64 files in `samples/` folder!

```bash
curl -X POST https://tamizh019-ai-voice-detection.hf.space/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "PASTE_BASE64_FROM_SAMPLES_FOLDER"
  }'
```

### Test with Postman

1. **Method**: `POST`
2. **URL**: `https://tamizh019-ai-voice-detection.hf.space/api/voice-detection`
3. **Headers**:
   - `Content-Type`: `application/json`
   - `x-api-key`: `YOUR_API_KEY`
4. **Body** (raw JSON):

```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "PASTE_BASE64_HERE"
}
```

**Sample files**: Use `samples/human_sample(Base64).txt` or `samples/AI_sample(Base64).txt`

---

## � Request & Response

**Request:**
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_STRING"
}
```

**Response:**
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.85,
  "explanation": "Strong synthetic spectral signature"
}
```

---

## ✨ Features

- 🎯 **AI Detection** - Identifies AI-generated voices
- 🌍 **5 Languages** - Tamil, English, Hindi, Malayalam, Telugu
- ⚡ **Fast** - Results in 2-5 seconds
- 🔒 **Secure** - API key authentication
- 📊 **Confidence Score** - 0.0 to 1.0 with explanation

---

## �️ Convert Your Own Audio

```bash
python utils/generate_base64.py "path/to/your/audio.mp3"
```

---

## 🧠 How It Works

Analyzes audio features using **librosa**:
- **Spectral Flatness** - AI voices are more uniform
- **Pitch Variation** - Humans vary naturally
- **Energy Patterns** - AI maintains steady volume
- **MFCCs** - Voice texture analysis

📚 **Detailed Docs:** [Docs/HOW_IT_WORKS.md](./Docs/HOW_IT_WORKS.md)

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/voice-detection` | POST | Classify audio |
| `/health` | GET | Health check |
| `/` | GET | API info |

**Authentication:** All requests require `x-api-key` header

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Uvicorn
- **Audio:** librosa, pydub, soundfile
- **ML:** NumPy, SciPy
- **Deployment:** Hugging Face Spaces (Docker)

---

**Built with ❤️ for the AI Voice Detection Hackathon**
