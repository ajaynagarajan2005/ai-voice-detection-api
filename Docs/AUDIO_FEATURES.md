# 🔊 Audio Features - Understanding What We Analyze

## Introduction

When you speak, your voice creates vibrations in the air. These vibrations can be captured as an audio file. Inside that file is a lot of hidden information about *how* the sound was produced.

AI voices and human voices produce sounds differently at a physical level. By extracting certain **features** from the audio, we can detect these differences.

---

## The Features We Extract

### 1. 🎵 MFCCs (Mel-Frequency Cepstral Coefficients)

**What it is:** A representation of the short-term power spectrum of sound, based on how human ears perceive frequencies.

**In simple terms:** Imagine taking a "fingerprint" of the voice's tone quality. MFCCs capture the unique "color" of a voice.

**Why it matters:** 
- Human voices have complex, varied MFCCs
- AI voices often have simpler, more uniform patterns

---

### 2. 📈 Spectral Flatness

**What it is:** A measure of how "noise-like" vs "tone-like" a sound is.

**In simple terms:** 
- **High flatness** = sounds like white noise (hissing)
- **Low flatness** = sounds like a clear tone (singing note)

**Why it matters:** This is our **strongest indicator**. AI voices tend to have very low spectral flatness variation, meaning they're "too clean" and consistent.

**Visual example:**
```
Human voice: ~~~∿∿∿~~~∿∿~~~∿  (varied)
AI voice:    ~~~~~~~~∿∿∿∿∿∿   (consistent)
```

---

### 3. 🎯 Spectral Centroid

**What it is:** The "center of mass" of the frequencies in the sound.

**In simple terms:** Is the voice mostly low-pitched, high-pitched, or balanced? Where is the "weight" of the sound?

**Why it matters:** Human voices shift their spectral centroid as we emphasize different words. AI voices may stay more centered.

---

### 4. 📉 Spectral Rolloff

**What it is:** The frequency below which 85% of the audio energy is contained.

**In simple terms:** It tells us where the "edge" of the voice's frequency range is.

**Why it matters:** Human voices have more natural high-frequency content from breathing, lip sounds, etc.

---

### 5. ⚡ RMS Energy

**What it is:** Root Mean Square energy - essentially the loudness of the audio.

**In simple terms:** How loud is the voice at any given moment?

**Why it matters:** 
- **Humans** naturally get louder and softer (emphasis, breathing, emotion)
- **AI voices** often maintain steady volume throughout

**Visual example:**
```
Human: ▃▅▇█▅▃▁▃▅▇█▅▃ (dynamic)
AI:    ▅▅▅▅▅▅▅▅▅▅▅▅▅ (flat)
```

---

### 6. 🎼 Pitch (Fundamental Frequency)

**What it is:** The main frequency of the voice - how high or low it sounds.

**In simple terms:** Think of it as the "note" someone is speaking on.

**What we measure:**
- **Pitch Mean**: Average pitch
- **Pitch Std**: How much pitch varies
- **Pitch Range**: Difference between highest and lowest

**Why it matters:** 
- Human speech naturally rises and falls (questions go up, statements go down)
- Early AI voices were very monotone, though modern ones try to mimic variation

---

### 7. 🥁 Zero Crossing Rate (ZCR)

**What it is:** How often the audio signal crosses the zero line (switches between positive and negative).

**In simple terms:** It's related to the "texture" and rhythm of the sound.

**Why it matters:** 
- Human speech has natural variation in rhythm
- AI voices can be too metronomic (perfectly timed)

---

### 8. 🌈 Spectral Contrast

**What it is:** The difference between peaks and valleys in the frequency spectrum.

**In simple terms:** Does the voice have strong contrasts between loud and quiet frequencies, or is it all blended together?

**Why it matters:** Human voices have more dynamic contrast. AI voices can be "flatter" in their spectral profile.

---

## How These Features Work Together

No single feature definitively says "AI" or "Human." It's the **combination** that matters:

| Feature | Strong AI Signal | Strong Human Signal |
|---------|-----------------|---------------------|
| Spectral Flatness Std | < 0.06 | > 0.15 |
| Pitch Std | < 50 Hz | > 200 Hz |
| RMS Std | < 0.02 | > 0.05 |
| ZCR Std | < 0.03 | > 0.08 |

When multiple features point in the same direction, confidence increases.

---

## The Technical Library: Librosa

We use a Python library called **librosa** to extract these features. Librosa is specifically designed for audio analysis and is used widely in music and speech processing.

```python
import librosa

# Load audio
y, sr = librosa.load("audio.mp3", sr=22050)

# Extract features
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
spectral_flatness = librosa.feature.spectral_flatness(y=y)
rms = librosa.feature.rms(y=y)
# ... and more
```

---

## Visualizing the Difference

If you could "see" audio, here's what AI vs Human might look like:

### Human Voice Spectrogram
```
Frequency ▲
          │ ██ ▄▄   ██ ▄▄   ██     <- Rich, varied patterns
          │▄██▀▀▄▄▄ ██▀▀▄▄▄██▄▄
          │████████▄██████████▄▄
          └─────────────────────▶ Time
```

### AI Voice Spectrogram
```
Frequency ▲
          │ ██████  ███████████   <- More uniform bands
          │████████████████████
          │████████████████████
          └─────────────────────▶ Time
```

---

## Summary

Our classifier works by measuring these audio features and looking for the subtle differences between synthetic and natural speech. The key insight is that AI voices, no matter how good, are still generated by algorithms that lack the natural imperfections of human biology.

---

## Further Reading

- [Librosa Documentation](https://librosa.org/doc/latest/)
- [Understanding MFCCs](https://en.wikipedia.org/wiki/Mel-frequency_cepstrum)
- [Speech Signal Processing](https://en.wikipedia.org/wiki/Speech_processing)
