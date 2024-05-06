import os
import cv2
import numpy as np
from PIL import Image
import mss
from skimage.metrics import structural_similarity as compare_ssim
from concurrent.futures import ThreadPoolExecutor

class CardDetector:
    def __init__(self, card_folder):
        self.card_folder = card_folder
        self.card_images = self.load_card_images()
        self.detected_cards = set()

    def load_card_images(self):
        card_images = {}
        for filename in os.listdir(self.card_folder):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                name = os.path.splitext(filename)[0]
                path = os.path.join(self.card_folder, filename)
                image = cv2.imread(path)
                card_images[name] = image
        return card_images

    def capture_secondary_display(self):
        try:
            with mss.mss() as sct:
                secondary_bbox = sct.monitors[2]
                screenshot = sct.grab(secondary_bbox)
                if screenshot:
                    img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                    return img
                else:
                    print("Error: Failed to capture screenshot.")
                    return None
        except Exception as e:
            print("Error capturing secondary display:", e)
            return None

    def get_pic_and_save(self):
        print("Capturing the secondary display...")
        screenshot = self.capture_secondary_display()
        if screenshot:
            try:
                width, height = screenshot.size
                top_percentage_to_remove = 0.08
                crop_top_height = int(height * top_percentage_to_remove)
                crop_width = width // 4.5
                crop_height = height // 4.5
                upper_right_box = (width - crop_width, crop_top_height, width, crop_height)
                upper_right = screenshot.crop(upper_right_box)
                upper_right.save("upper_right_secondary_display.png")
                print("Upper right part of the secondary display saved as 'upper_right_secondary_display.png'")

                # Convert the PIL image to OpenCV format
                opencv_image = np.array(upper_right)
                opencv_image = opencv_image[:, :, ::-1].copy()  # Convert RGB to BGR

                # Detect cards in the image
                self.detect_cards(opencv_image)
            except Exception as e:
                print("Error processing captured image:", e)
        else:
            print("Unable to capture the secondary display.")

    def detect_cards(self, image):
        print("Detecting cards...")
        # Resize card images to match the dimensions of the captured image
        resized_card_images = {}
        for name, card_image in self.card_images.items():
            resized_card_image = cv2.resize(card_image, (image.shape[1], image.shape[0]))
            resized_card_images[name] = resized_card_image

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Perform edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Resize detected cards to match the size of card images
        resized_detected_cards = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            card = image[y:y+h, x:x+w]
            resized_card = cv2.resize(card, (image.shape[1], image.shape[0]))  # Assuming width and height are dimensions of card images
            resized_detected_cards.append(resized_card)

        # Compare detected cards with resized card images
        with ThreadPoolExecutor() as executor:
            futures = []
            for detected_card in resized_detected_cards:
                future = executor.submit(self.compare_images, detected_card, resized_card_images)
                futures.append(future)
            for future in futures:
                best_match_name, best_match_similarity = future.result()
                if best_match_similarity > 0.6:  # Adjust similarity threshold as needed
                    self.detected_cards.add(best_match_name)
                    print(f"Detected card: {best_match_name} (Similarity: {best_match_similarity})")
        print("Card detection complete.")

    def compare_images(self, detected_card, resized_card_images):
        best_match_name = None
        best_match_similarity = 0
        for name, card_image in resized_card_images.items():
            similarity = self.compare_image(detected_card, card_image)
            if similarity > best_match_similarity:
                best_match_name = name
                best_match_similarity = similarity
        return best_match_name, best_match_similarity

    def compare_image(self, image1, image2):
        # Calculate the Structural Similarity Index (SSI) between two images
        # You may use other image similarity metrics depending on your requirements
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        similarity_index = compare_ssim(gray1, gray2)
        return similarity_index

    def print_remaining_cards(self):
        standard_deck = {
            'Ace of Spades', 'Two of Spades', 'Three of Spades', 'Four of Spades', 'Five of Spades', 'Six of Spades', 'Seven of Spades', 'Eight of Spades', 'Nine of Spades', 'Ten of Spades', 'Jack of Spades', 'Queen of Spades', 'King of Spades',
            'Ace of Hearts', 'Two of Hearts', 'Three of Hearts', 'Four of Hearts', 'Five of Hearts', 'Six of Hearts', 'Seven of Hearts', 'Eight of Hearts', 'Nine of Hearts', 'Ten of Hearts', 'Jack of Hearts', 'Queen of Hearts', 'King of Hearts',
            'Ace of Clubs', 'Two of Clubs', 'Three of Clubs', 'Four of Clubs', 'Five of Clubs', 'Six of Clubs', 'Seven of Clubs', 'Eight of Clubs', 'Nine of Clubs', 'Ten of Clubs', 'Jack of Clubs', 'Queen of Clubs', 'King of Clubs',
            'Ace of Diamonds', 'Two of Diamonds', 'Three of Diamonds', 'Four of Diamonds', 'Five of Diamonds', 'Six of Diamonds', 'Seven of Diamonds', 'Eight of Diamonds', 'Nine of Diamonds', 'Ten of Diamonds', 'Jack of Diamonds', 'Queen of Diamonds', 'King of Diamonds'
        }
        remaining_cards = standard_deck - self.detected_cards
        print("Remaining cards:")
        for card in remaining_cards:
            print(card)

    def main(self):
        # Call the function to capture and save the image
        self.get_pic_and_save()
        # Print the remaining cards
        self.print_remaining_cards()

if __name__ == "__main__":
    card_detector = CardDetector(card_folder="cards")
    card_detector.main()
