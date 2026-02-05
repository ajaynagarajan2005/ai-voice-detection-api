# 🎤 AI Voice Detection - Project Overview

## What Does This Project Do?

This project is an **AI-powered API** that listens to audio recordings and determines whether the voice is:
- **AI-Generated** (created by text-to-speech systems, voice cloning, etc.)
- **Human** (spoken by a real person)

Think of it like a "lie detector" for voices — except instead of detecting lies, it detects whether the voice is synthetic or natural.

---

## Why Is This Important?

With the rise of AI voice generators (like ElevenLabs, Google TTS, etc.), it's becoming harder to tell if:
- A phone call is from a real person or a scam bot
- An audio message is genuine or fabricated
- A voice recording has been manipulated

This API provides a **quick, automated check** to help verify voice authenticity.

---

## How It Works (Simple Version)

```
[Audio File] → [Extract Features] → [Analyze Patterns] → [AI or Human?]
```

1. **You send** an audio file (as Base64-encoded MP3)
2. **The API extracts** acoustic features (pitch, rhythm, energy, etc.)
3. **The classifier scores** these features against known AI vs. Human patterns
4. **You receive** a classification with a confidence score

---

## Supported Languages

The API works with **5 languages**:
- 🇮🇳 Tamil
- 🇬🇧 English
- 🇮🇳 Hindi
- 🇮🇳 Malayalam
- 🇮🇳 Telugu

**Note:** The detection is actually *language-agnostic* because it analyzes the physical properties of sound waves, not the words being spoken. The language field is for your reference and logging.

---

## Key Features

| Feature | Description |
|---------|-------------|
| **Real Analysis** | No hardcoding - every audio is genuinely analyzed |
| **Fast Response** | Results in 2-5 seconds |
| **Secure** | API key authentication required |
| **Confidence Score** | 0.0 to 1.0 indicating certainty |
| **Explanation** | Human-readable reason for the decision |

---

## Example Response

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

## What Makes AI Voices Different?

AI-generated voices, even high-quality ones, have subtle "tells":

1. **Too Perfect** - Consistent pitch and rhythm (humans naturally vary)
2. **Flat Spectrum** - Less variation in frequency distribution
3. **Uniform Energy** - Steady volume (humans breathe, pause, emphasize)

Our classifier looks for these patterns to make its decision.

---

## Next Steps

- **[HOW_IT_WORKS.md](./HOW_IT_WORKS.md)** - Deep dive into the detection logic
- **[API_GUIDE.md](./API_GUIDE.md)** - How to use the API
- **[AUDIO_FEATURES.md](./AUDIO_FEATURES.md)** - Understanding the audio analysis
