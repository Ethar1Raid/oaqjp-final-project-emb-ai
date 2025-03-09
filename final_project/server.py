"""
Server module for deploying the EmotionDetection application using Flask.

This module sets up the Flask web server and provides endpoints to render the home page
and process emotion detection requests.
"""

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route('/')
def home():
    """
    Render the home page of the EmotionDetection application.

    Returns:
        str: Rendered HTML for the index page.
    """
    return render_template('index.html')


@app.route('/emotionDetector', methods=['POST'])
def emotionDetector():
    """
    Process an emotion detection request.

    Retrieves the 'statement' parameter from the submitted form, calls the
    emotion_detector function, and returns a formatted response. If the input is
    invalid (blank or whitespace-only) or the dominant emotion cannot be determined,
    an error message is returned.

    Returns:
        tuple or str: A formatted response string with emotion scores and the dominant emotion,
                      or an error message with a 400 status code if input is invalid.
    """
    statement = request.form.get('statement')
    if not statement or statement.strip() == "":
        return "Invalid text! Please try again!", 400

    results = emotion_detector(statement)

    if results.get('dominant_emotion') is None:
        return "Invalid text! Please try again!", 400

    response_text = (
        f"For the given statement, the system response is 'anger': {results['anger']}, "
        f"'disgust': {results['disgust']}, 'fear': {results['fear']}, "
        f"'joy': {results['joy']} and 'sadness': {results['sadness']}. "
        f"The dominant emotion is {results['dominant_emotion']}."
    )
    return response_text


if __name__ == '__main__':
    """
    Run the Flask development server on localhost:5000.
    """
    app.run(host="localhost", port=5000, debug=True)
