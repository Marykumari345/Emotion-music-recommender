import os
print("Running file:", os.path.abspath(__file__))

print("Flask app is starting...")
from flask import Flask, render_template, request
from fer import FER
import cv2
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # ✅ Check if image exists in request
    if 'image' not in request.files:
        return render_template('index.html', error='No image uploaded')

    image = request.files['image']

    # ✅ Create folder if missing
    os.makedirs('static/images', exist_ok=True)

    # ✅ Check empty filename
    if image.filename == '':
        return render_template('index.html', error='No file selected')

    # ✅ Save image
    path = os.path.join('static/images', image.filename)
    image.save(path)

    # ✅ Emotion detection
    detector = FER(mtcnn=True)
    img = cv2.imread(path)
    emotions = detector.detect_emotions(img)

    if emotions:
        emotion = max(emotions[0]["emotions"], key=emotions[0]["emotions"].get)
    else:
        emotion = "neutral"

    # ✅ Load songs
    with open('songs.json') as f:
        songs = json.load(f)

    # ✅ Send emotion + songs to HTML
    return render_template('index.html', emotion=emotion, songs=songs.get(emotion, []))

if __name__ == '__main__':
    app.run(debug=True)
