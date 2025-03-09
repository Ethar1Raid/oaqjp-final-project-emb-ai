import requests
import json

def emotion_detector(text_to_analyze):
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {
        "grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"
    }
    payload = {
        "raw_document": {
            "text": text_to_analyze
        }
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    # If the API returns a 400 status code (e.g., due to blank input), return a dictionary with None values.
    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }
    
    response.raise_for_status()
    response_data = response.json()

    if "text" in response_data:
        text_response = response_data.get("text")
        try:
            emotion_data = json.loads(text_response)
        except json.JSONDecodeError:
            raise ValueError("Response text is not valid JSON.")
    elif "emotionPredictions" in response_data and response_data["emotionPredictions"]:
        emotion_data = response_data["emotionPredictions"][0].get("emotion", {})
    else:
        raise ValueError("Response does not contain expected emotion predictions.")

    # Extract emotion scores (defaulting to 0 if not found)
    anger_score = emotion_data.get("anger", 0)
    disgust_score = emotion_data.get("disgust", 0)
    fear_score = emotion_data.get("fear", 0)
    joy_score = emotion_data.get("joy", 0)
    sadness_score = emotion_data.get("sadness", 0)

    scores = {
        'anger': anger_score,
        'disgust': disgust_score,
        'fear': fear_score,
        'joy': joy_score,
        'sadness': sadness_score,
    }
    
    # Determine the dominant emotion if there is any non-zero score; otherwise, set to None.
    dominant_emotion = max(scores, key=scores.get) if any(scores.values()) else None
    scores['dominant_emotion'] = dominant_emotion
    
    return scores
