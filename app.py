from flask import Flask, request, jsonify
import speech_recognition as sr
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the MP3 to Lyrics Generator!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})

    if file and allowed_file(file.filename):
        audio_text = process_audio(file)
        return jsonify({"lyrics": audio_text})
    return jsonify({"error": "Invalid file format"})

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'mp3'}

def process_audio(file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file) as source:
        audio_data = recognizer.record(source)
    try:
        # Using Google's speech recognition
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

if __name__ == '__main__':
    app.run(debug=True)
