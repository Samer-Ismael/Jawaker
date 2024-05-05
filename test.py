import os
import cv2
import numpy as np
from PIL import Image
import mss
from skimage.metrics import structural_similarity as compare_ssim

class CardDetector:
    def __init__(self, card_folder):
        self.card_folder = card_folder
        self.card_images = self.load_card_images()
        self.width = None
        self.height = None

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
                    return img, img.size[0], img.size[1]
                else:
                    print("Error: Failed to capture screenshot.")
                    return None, None, None
        except Exception as e:
            print("Error capturing secondary display:", e)
            return None, None, None

    def get_pic_and_save(self):
        print("Capturing the secondary display...")
        screenshot, width, height = self.capture_secondary_display()
        if screenshot:
            try:
                self.width = width
                self.height = height
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
        # Resize card images to match the dimensions of the captured image
        resized_card_images = {}
        for name, card_image in self.card_images.items():
            resized_card_image = cv2.resize(card_image, (self.width, self.height))
            resized_card_images[name] = resized_card_image

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Perform edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edge-detected image
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Draw contours on the original image for visualization
        cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

        # Resize detected cards to match the size of card images
        resized_detected_cards = {}
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            card = image[y:y+h, x:x+w]
            resized_card = cv2.resize(card, (self.width, self.height))  # Assuming width and height are dimensions of card images
            resized_detected_cards[i] = resized_card

        # Compare detected cards with resized card images
        for i, detected_card in resized_detected_cards.items():
            best_match_name = None
            best_match_similarity = 0
            for name, card_image in resized_card_images.items():
                similarity = self.compare_images(detected_card, card_image)
                if similarity > best_match_similarity:
                    best_match_name = name
                    best_match_similarity = similarity
            print(f"Detected card {i+1}: {best_match_name} (Similarity: {best_match_similarity})")

    def compare_images(self, image1, image2):
        # Calculate the Structural Similarity Index (SSI) between two images
        # You may use other image similarity metrics depending on your requirements
        gray1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        similarity_index = compare_ssim(gray1, gray2)
        return similarity_index

    def main(self):
        # Call the function to capture and save the image
        self.get_pic_and_save()

if __name__ == "__main__":
    card_detector = CardDetector(card_folder="cards")
    card_detector.main()
