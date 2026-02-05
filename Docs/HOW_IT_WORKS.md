# 🧠 How It Works - The Detection Logic

## The Big Picture

When you send an audio file, the API doesn't just "guess" whether it's AI or human. It goes through a systematic analysis process:

```
Audio → Feature Extraction → Rule-Based Scoring → Classification
```

---

## Step 1: Feature Extraction

The first thing we do is convert the audio into **numbers** that describe its characteristics. Using a library called `librosa`, we extract:

### 🎵 Pitch Features
- **Pitch Mean**: The average "highness" or "lowness" of the voice
- **Pitch Variation (Std)**: How much the pitch changes during speech
- **Pitch Range**: The difference between highest and lowest pitch

*Why it matters:* Human speech naturally goes up and down (think of asking a question vs. making a statement). AI voices often have more consistent pitch.

### 📊 Spectral Features
- **Spectral Flatness**: How "noisy" vs. "tonal" the sound is
- **Spectral Centroid**: The "center of mass" of the frequencies
- **Spectral Rolloff**: Where most of the energy is concentrated

*Why it matters:* AI voices tend to have flatter, more uniform spectra. Human voices have more variation and "texture."

### ⚡ Energy Features
- **RMS Mean**: Average loudness
- **RMS Variation**: How much the volume changes

*Why it matters:* Humans naturally get louder and softer. AI voices often maintain steady volume.

### 🥁 Rhythm Features
- **Zero Crossing Rate (ZCR)**: How often the audio signal crosses zero
- **ZCR Variation**: How consistent the rhythm is

*Why it matters:* Human speech has natural pauses, breaths, and emphasis. AI speech is often more metronomic.

---

## Step 2: The Scoring System

Once we have the features, we use a **rule-based scoring system** to decide:

```python
ai_score = 0
human_score = 0

# Example Rule: Spectral Flatness
if spectral_flatness_std < 0.06:
    ai_score += 4  # Very flat = likely AI
else:
    human_score += 1  # More variation = likely human
```

### Our Key Rules:

| Rule | AI Indicator | Human Indicator |
|------|-------------|-----------------|
| **Spectral Flatness** | Low variation (< 0.06) | High variation |
| **Pitch Consistency** | Very consistent (std < 50) | Natural variation |
| **Energy Variation** | Steady volume | Dynamic volume |
| **Rhythm Patterns** | Uniform | Natural pauses |

### The Override

We have a special rule: If spectral flatness is **extremely low** (< 0.06), this is such a strong AI indicator that we add **extra points** to the AI score. This catches even high-quality AI voices that try to mimic human variation.

---

## Step 3: Classification

After all rules are applied, we compare scores:

```python
if ai_score > human_score:
    classification = "AI_GENERATED"
else:
    classification = "HUMAN"
```

### Confidence Score

The confidence score tells you how certain the classifier is:

```python
confidence = max(ai_score, human_score) / (ai_score + human_score)
```

- **0.55-0.65**: Close call, could go either way
- **0.65-0.80**: Reasonably confident
- **0.80-0.95**: Very confident

---

## Why Rule-Based Instead of Machine Learning?

Great question! We chose rule-based heuristics because:

1. **Speed**: No need to train on thousands of samples
2. **Interpretability**: We can explain *why* a decision was made
3. **Hackathon Constraints**: 5-hour time limit
4. **Robustness**: Works without labeled training data

A full ML approach (neural networks, etc.) would require:
- Large datasets of AI and human voices
- Training time
- More computational resources

For this hackathon, rule-based was the practical choice.

---

## Real Example

When we tested `sample voice 1.mp3` (known AI-generated):

```
Features Detected:
- Spectral Flatness Std: 0.0541 (very low!)
- Pitch Std: 857 (high variation - AI trying to sound human)
- RMS Std: 0.0646 (moderate)

Scores:
- AI Score: 10 (mainly from spectral flatness)
- Human Score: 7

Result: AI_GENERATED (Confidence: 0.59)
```

The low spectral flatness was the "tell" that revealed the synthetic origin.

---

## Limitations

Our classifier isn't perfect:

- **High-quality AI voices** may fool it (especially those trained on specific individuals)
- **Very short audio** has less data to analyze
- **Noisy recordings** can obscure the features
- **Edge cases** like voice changers or heavy processing

But for most common AI voice generators, it works well!

---

## Learn More

- **[AUDIO_FEATURES.md](./AUDIO_FEATURES.md)** - Detailed explanation of each feature
- **[PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)** - High-level project summary
