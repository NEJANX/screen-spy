import cv2
import numpy as np
import pyautogui
from flask import Flask, Response, render_template_string

app = Flask(__name__)

def generate_frames():
    while True:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head>
            <title>Screen Cast</title>
        </head>
        <body>
            <h1>Screen Cast</h1>
            <img src="{{ url_for('video_feed') }}" style="max-width: 100%; height: auto;">
        </body>
        </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
