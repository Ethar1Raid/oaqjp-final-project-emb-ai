import requests

def emotion_detector(text_to_analyze):
    """
    Function that uses the Watson NLP Library to analyze emotions in a text,
    with error handling for empty inputs.
    """
    if not text_to_analyze:  # Checks if the text is empty
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'}
    input_json = {
        'raw_document': {
            'text': text_to_analyze
        }
    }

    try:
        response = requests.post(url, headers=headers, json=input_json)
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

        emotions = response_data.get('emotion_predictions', {})
        emotion_scores = {
            'anger': emotions.get('anger', 0),
            'disgust': emotions.get('disgust', 0),
            'fear': emotions.get('fear', 0),
            'joy': emotions.get('joy', 0),
            'sadness': emotions.get('sadness', 0)
        }
        emotion_scores['dominant_emotion'] = max(emotion_scores, key=emotion_scores.get)
        return emotion_scores

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Watson NLP API: {e}")
        return None
