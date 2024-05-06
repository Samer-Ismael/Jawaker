from flask import Flask, jsonify, send_file
from card_detector import CardDetector
import time
import threading

app = Flask(__name__)

# Initialize CardDetector instance
card_detector = CardDetector(card_folder="cards")

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
    app.run(debug=True)
