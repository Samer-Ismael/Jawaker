from flask import Flask, jsonify
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

if __name__ == '__main__':
    # Start a separate thread for card detection
    threading.Thread(target=run_card_detection, daemon=True).start()
    app.run(debug=True)
