import os

from flask import Flask, jsonify, send_file, redirect, send_from_directory
from flask_cors import CORS
import threading
import time

from card_detector import CardDetector

app = Flask(__name__)
CORS(app)
# Initialize CardDetector instance
card_detector = CardDetector(card_folder="cards")


# Define the path to the HTML file in the frontend folder
frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')


@app.route('/')
def index():
    # Send the HTML file to the client
    return send_file(os.path.join(frontend_dir, 'index.html'))

@app.route('/<path:filename>')
def serve_static(filename):
    # Serve static files (CSS, JavaScript, etc.) from the frontend directory
    return send_from_directory(frontend_dir, filename)

@app.route('/cards')
def get_detected_cards():
    detected_cards = card_detector.get_detected_cards()
    return jsonify(detected_cards)

def run_card_detection():
    while True:
        card_detector.get_pic_and_save()
        time.sleep(1)

@app.route('/picture')
def get_picture():
    # Set the path to the picture here
    picture_path = "upper_right_secondary_display.png"

    return send_file(picture_path, mimetype='image/png')

if __name__ == '__main__':
    # Start a separate thread for card detection
    threading.Thread(target=run_card_detection, daemon=True).start()
    app.run(debug=True, port=5001)
