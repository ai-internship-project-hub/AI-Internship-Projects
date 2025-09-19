# ✅ Step 1: Install required libraries
!pip install flask opencv-python --quiet

# ✅ Step 2: Save the Flask app with OpenCV
code = """
from flask import Flask, render_template, Response
import cv2
import os

# Flask app
app = Flask(__name__)
cap = cv2.VideoCapture(0)

# Load Haar cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

eyes_closed_frames = 0
alert_triggered = False

# Generate camera frames
def gen_frames():
    global eyes_closed_frames, alert_triggered
    while True:
        success, frame = cap.read()
        if not success:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        eye_detected = False

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                eye_detected = True

        if not eye_detected:
            eyes_closed_frames += 1
        else:
            eyes_closed_frames = 0
            alert_triggered = False

        if eyes_closed_frames >= 60 and not alert_triggered:
            cv2.putText(frame, "ALERT: Eyes closed too long!", (30, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)
            alert_triggered = True

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\\r\\n'
               b'Content-Type: image/jpeg\\r\\n\\r\\n' + frame + b'\\r\\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=False)
"""

with open("eye_alert_app.py", "w", encoding='utf-8') as f:
    f.write(code)

# ✅ Step 3: Save the HTML template
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>AI Eye Strain Monitor</title>
    <style>
        body { text-align: center; font-family: Arial; background: #f0f0f0; }
        h1 { color: #333; }
        img { border: 4px solid #2a9df4; margin-top: 20px; width: 80%; max-width: 640px; }
    </style>
</head>
<body>
    <h1>AI Eye Strain Alert System</h1>
    <img src="{{ url_for('video') }}" alt="Live Feed">
</body>
</html>
"""

import os
os.makedirs("templates", exist_ok=True)
with open("templates/index.html", "w", encoding='utf-8') as f:
    f.write(html_code)

# ✅ Step 4: Run the Flask app
!python eye_alert_app.py
