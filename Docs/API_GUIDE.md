# 📡 API Guide - Using the Voice Detection API

## Quick Start

### Base URL
```
https://tamizh019-ai-voice-detection.hf.space
```

### Endpoint
```
POST /api/voice-detection
```

---

## Authentication

Every request must include an API key in the header:

```
x-api-key: YOUR_API_KEY
```

Without this header, you'll receive a `401 Unauthorized` error.

---

## Request Format

### Headers
```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

### Body (JSON)
```json
{
  "language": "English",
  "audioFormat": "mp3",
  "audioBase64": "BASE64_ENCODED_AUDIO_STRING"
}
```

### Fields Explained

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `language` | string | Yes | One of: Tamil, English, Hindi, Malayalam, Telugu |
| `audioFormat` | string | Yes | Must be "mp3" |
| `audioBase64` | string | Yes | Your audio file encoded as Base64 |

---

## Response Format

### Success Response (200 OK)
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.85,
  "explanation": "Strong synthetic spectral signature"
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | "success" or "error" |
| `language` | string | The language you specified |
| `classification` | string | "AI_GENERATED" or "HUMAN" |
| `confidenceScore` | float | 0.0 to 1.0 (higher = more confident) |
| `explanation` | string | Human-readable reason for the decision |

---

## Error Responses

### 401 - Unauthorized
```json
{
  "status": "error",
  "message": "Invalid or missing API key"
}
```

### 400 - Bad Request
```json
{
  "status": "error",
  "message": "Invalid language. Must be one of: Tamil, English, Hindi, Malayalam, Telugu"
}
```

### 500 - Server Error
```json
{
  "status": "error",
  "message": "Processing failed: [error details]"
}
```

---

## How to Convert Audio to Base64

### Using Python
```python
import base64

with open("your_audio.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode("utf-8")

print(audio_base64)
```

### Using Our Helper Script
```bash
python generate_base64.py "path/to/your/audio.mp3"
```

This will print the Base64 string and save it to `base64_output.txt`.

---

## Complete Example

### Using cURL
```bash
curl -X POST https://tamizh019-ai-voice-detection.hf.space/api/voice-detection \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "SUQzBAAAAAAAI1RTU0UAAAAOAAADTGF2ZjYwLjE2LjEwMEdFT0..."
  }'
```

### Using Python
```python
import requests
import base64

# Read your audio file
with open("sample.mp3", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

# Make the request
response = requests.post(
    "https://tamizh019-ai-voice-detection.hf.space/api/voice-detection",
    headers={
        "Content-Type": "application/json",
        "x-api-key": "YOUR_API_KEY"
    },
    json={
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
)

print(response.json())
```

### Using Postman
1. Create a new **POST** request
2. URL: `https://tamizh019-ai-voice-detection.hf.space/api/voice-detection`
3. Headers tab:
   - `Content-Type`: `application/json`
   - `x-api-key`: `YOUR_API_KEY`
4. Body tab:
   - Select "raw" and "JSON"
   - Paste your JSON body
5. Click Send

---

## Other Endpoints

### Health Check
```
GET /health
```
Returns: `{"status": "healthy", "message": "API is running"}`

Use this to check if the API is online.

### Root
```
GET /
```
Returns API information and available endpoints.

---

## Rate Limits & Constraints

| Constraint | Value |
|------------|-------|
| Max file size | 10 MB |
| Min file size | 1 KB |
| Audio format | MP3 only |
| Response time | 2-5 seconds |

---

## Tips for Best Results

1. **Use clear audio** - Avoid background noise
2. **Longer is better** - At least 3-5 seconds of speech
3. **MP3 format** - Convert other formats before sending
4. **Check confidence** - Scores below 0.65 are uncertain

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| 401 Error | Check your API key is correct |
| 400 Error | Verify language is one of the 5 supported |
| Empty response | Ensure Base64 encoding is correct |
| Slow response | Large files take longer; try compressing |
| Wrong classification | Some edge cases may be misclassified |
