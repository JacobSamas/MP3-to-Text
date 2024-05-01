from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
import speech_recognition as sr
from pydub import AudioSegment
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def process_audio(file_path):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_mp3(file_path)
    audio.export("temp.wav", format="wav")
    audio_path = "temp.wav"
    
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio_data)
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results; {e}"

@app.route('/')
def home():
    return render_template('index.html')  # Renders index.html as the main page

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        lyrics = process_audio(file_path)
        return jsonify({"lyrics": lyrics})
    return jsonify({"error": "Invalid file format"})

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
