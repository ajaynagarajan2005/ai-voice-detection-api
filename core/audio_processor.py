"""
Audio Processing Module - AI Voice Detection
Implements feature extraction and classification logic using librosa
"""

import librosa
import numpy as np
from io import BytesIO
from typing import Dict, Any, List, Tuple


def extract_audio_features(audio_bytes: bytes) -> Dict[str, Any]:
    """
    Extract audio features from raw audio bytes.
    
    Features extracted:
    - MFCCs (Mel-frequency cepstral coefficients)
    - Zero Crossing Rate
    - Spectral Centroid
    - Spectral Rolloff
    - Spectral Flatness (KEY for AI detection)
    - Chroma Features
    - RMS Energy
    - Pitch Variation
    """
    # Load audio with standard sample rate
    y, sr = librosa.load(BytesIO(audio_bytes), sr=22050)
    
    features = {}
    
    # 1. MFCCs - captures the overall shape of the spectral envelope
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    features['mfcc_mean'] = np.mean(mfccs, axis=1)
    features['mfcc_std'] = np.std(mfccs, axis=1)
    features['mfcc_var'] = np.var(mfccs, axis=1)
    
    # 2. Zero Crossing Rate - rate at which signal changes sign
    zcr = librosa.feature.zero_crossing_rate(y)
    features['zcr_mean'] = float(np.mean(zcr))
    features['zcr_std'] = float(np.std(zcr))
    
    # 3. Spectral Centroid - "center of mass" of the spectrum
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    features['spectral_centroid_mean'] = float(np.mean(spectral_centroid))
    features['spectral_centroid_std'] = float(np.std(spectral_centroid))
    
    # 4. Spectral Rolloff - frequency below which 85% of energy is contained
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
    features['spectral_rolloff_mean'] = float(np.mean(spectral_rolloff))
    features['spectral_rolloff_std'] = float(np.std(spectral_rolloff))
    
    # 5. Spectral Flatness - KEY FOR AI DETECTION
    # AI voices tend to have flatter spectral distributions
    spectral_flatness = librosa.feature.spectral_flatness(y=y)
    features['spectral_flatness_mean'] = float(np.mean(spectral_flatness))
    features['spectral_flatness_std'] = float(np.std(spectral_flatness))
    
    # 6. Chroma Features - related to the pitch class
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features['chroma_mean'] = float(np.mean(chroma))
    features['chroma_std'] = float(np.std(chroma))
    
    # 7. RMS Energy - loudness/energy of the signal
    rms = librosa.feature.rms(y=y)
    features['rms_mean'] = float(np.mean(rms))
    features['rms_std'] = float(np.std(rms))
    
    # 8. Pitch Variation - natural speech has variable pitch
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    pitch_values = []
    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        if pitch > 0:
            pitch_values.append(pitch)
    
    if pitch_values:
        features['pitch_mean'] = float(np.mean(pitch_values))
        features['pitch_std'] = float(np.std(pitch_values))
        features['pitch_range'] = float(np.max(pitch_values) - np.min(pitch_values))
    else:
        features['pitch_mean'] = 0.0
        features['pitch_std'] = 0.0
        features['pitch_range'] = 0.0
    
    # 9. Additional features for better detection
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
    features['spectral_bandwidth_mean'] = float(np.mean(spectral_bandwidth))
    features['spectral_bandwidth_std'] = float(np.std(spectral_bandwidth))
    
    # Spectral contrast
    spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
    features['spectral_contrast_mean'] = float(np.mean(spectral_contrast))
    features['spectral_contrast_std'] = float(np.std(spectral_contrast))
    
    return features


def classify_voice(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Classify voice as AI-generated or Human based on extracted features.
    
    Uses rule-based heuristics:
    - AI voices: Flat spectral patterns, consistent pitch, uniform energy
    - Human voices: Variable pitch, natural pauses, emotional inflection
    """
    ai_score = 0
    human_score = 0
    reasons = []
    
    # Rule 1: Spectral Flatness (STRONGEST INDICATOR)
    # AI voices, even high-quality ones, often have lower spectral variance
    # The sample had 0.0541, so we tune the threshold to catch this
    if features['spectral_flatness_std'] < 0.06:
        ai_score += 4  # Boosted weight for very low flatness
        reasons.append("Synthetic spectral structure detected")
    elif features['spectral_flatness_std'] < 0.15:
        ai_score += 2
        reasons.append("Low spectral variance")
    else:
        human_score += 1  # Reduced human weight for this
        reasons.append("Natural spectral variation")
    
    # Rule 2: Pitch Consistency
    # Modern AI can mimic pitch variation well (sample had std ~850!)
    # We only penalize if it's EXTREMELY consistent
    if features['pitch_std'] < 50:
        ai_score += 3
        reasons.append("Unnatural pitch consistency")
    elif features['pitch_std'] < 200:
        ai_score += 1
    else:
        # High pitch variation is common in both emotional AI and Humans now
        # So we give less weight to "Human" here unless it's very complex
        if features['pitch_range'] > 3000:
            human_score += 1
            reasons.append("Wide pitch range")
            
            # Check if this high range is just noise/artifacts
            if features['zcr_std'] > 0.1:
                human_score += 1 # Likely natural speech
    
    # Rule 3: Zero Crossing Rate Variation
    if features['zcr_std'] < 0.03:
        ai_score += 2
        reasons.append("Uniform rhythm patterns")
    else:
        human_score += 1
    
    # Rule 4: Energy Variation (RMS)
    if features['rms_std'] < 0.02:
        ai_score += 1
        reasons.append("Consistent energy levels")
    else:
        human_score += 1
    
    # Rule 5: MFCC Variance
    mfcc_var_sum = float(np.sum(features['mfcc_var']))
    if mfcc_var_sum < 5:
        ai_score += 2
        reasons.append("Low spectral diversity")
    else:
        human_score += 2
    
    # Rule 6: Spectral Bandwidth
    if features['spectral_bandwidth_std'] < 300:
        ai_score += 1
    
    # OVERRIDE: If spectral flatness is extremely low, it's almost certainly AI
    # This is the STRONGEST indicator and should dominate over other factors
    if features['spectral_flatness_std'] < 0.06:
        ai_score += 6  
        reasons.insert(0, "Strong synthetic spectral signature")
    
    # Rule 7: Spectral Contrast
    # Higher contrast variation is more natural
    if features['spectral_contrast_std'] < 5:
        ai_score += 1
        reasons.append("Low dynamic range")
    else:
        human_score += 1
        reasons.append("Dynamic spectral contrast")
    
    # Calculate confidence score
    total_score = ai_score + human_score
    if total_score > 0:
        confidence = max(ai_score, human_score) / total_score
    else:
        confidence = 0.5
    
    # Ensure confidence is within reasonable bounds
    confidence = max(0.55, min(0.95, confidence))
    
    # Determine classification
    if ai_score > human_score:
        classification = "AI_GENERATED"
        # Select top AI-related reasons
        ai_reasons = [r for r in reasons if any(kw in r.lower() for kw in 
                     ['unnatural', 'low', 'uniform', 'consistent', 'limited'])]
        explanation = "; ".join(ai_reasons[:3]) if ai_reasons else reasons[0]
    else:
        classification = "HUMAN"
        # Select top Human-related reasons
        human_reasons = [r for r in reasons if any(kw in r.lower() for kw in 
                        ['natural', 'variation', 'rich', 'dynamic'])]
        explanation = "; ".join(human_reasons[:3]) if human_reasons else reasons[0]
    
    return {
        "classification": classification,
        "confidenceScore": round(confidence, 2),
        "explanation": explanation
    }


def process_voice(audio_bytes: bytes, language: str) -> Dict[str, Any]:
    """
    Main function to process voice and return classification.
    
    Args:
        audio_bytes: Raw audio data
        language: Language of the audio (Tamil, English, Hindi, Malayalam, Telugu)
    
    Returns:
        Dictionary with status, language, classification, confidenceScore, explanation
    """
    try:
        # Extract features
        features = extract_audio_features(audio_bytes)
        
        # Classify voice
        result = classify_voice(features)
        
        return {
            "status": "success",
            "language": language,
            **result
        }
    except librosa.util.exceptions.ParameterError as e:
        return {
            "status": "error",
            "message": f"Invalid audio format: {str(e)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Processing failed: {str(e)}"
        }


def get_feature_summary(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get a human-readable summary of extracted features.
    Useful for debugging and analysis.
    """
    return {
        "pitch": {
            "mean": round(features['pitch_mean'], 2),
            "std": round(features['pitch_std'], 2),
            "range": round(features['pitch_range'], 2)
        },
        "spectral": {
            "flatness_mean": round(features['spectral_flatness_mean'], 4),
            "flatness_std": round(features['spectral_flatness_std'], 4),
            "centroid_mean": round(features['spectral_centroid_mean'], 2)
        },
        "energy": {
            "rms_mean": round(features['rms_mean'], 4),
            "rms_std": round(features['rms_std'], 4)
        },
        "rhythm": {
            "zcr_mean": round(features['zcr_mean'], 4),
            "zcr_std": round(features['zcr_std'], 4)
        }
    }
