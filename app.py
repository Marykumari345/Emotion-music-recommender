import os
import cv2
import json
from flask import Flask, render_template, request

app = Flask(__name__)

# ✅ Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'image' not in request.files:
        return render_template('index.html', error='No image uploaded')

    image = request.files['image']
    os.makedirs('static/images', exist_ok=True)

    if image.filename == '':
        return render_template('index.html', error='No file selected')

    path = os.path.join('static/images', image.filename)
    image.save(path)

    # ✅ Detect faces
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # ✅ Simple emotion logic (placeholder)
    if len(faces) > 0:
        emotion = "happy"   # You can expand this logic later
    else:
        emotion = "neutral"

    # ✅ Load songs.json
    with open('songs.json') as f:
        songs = json.load(f)

    return render_template('index.html', emotion=emotion, songs=songs.get(emotion, []))

if __name__ == '__main__':
    app.run(debug=True)
