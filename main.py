import requests
import json
import base64
from PIL import Image
import mss
import cv2
import numpy as np

def capture_secondary_display():
    try:
        with mss.mss() as sct:
            secondary_bbox = sct.monitors[2]
            screenshot = sct.grab(secondary_bbox)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            return img
    except Exception as e:
        print("Error capturing secondary display:", e)
        return None

def detect_cards(image):
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

    # Display the result
    cv2.imshow('Card Detection', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_pic_and_save():
    print("Capturing the secondary display...")
    screenshot = capture_secondary_display()
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
            detect_cards(opencv_image)
        except Exception as e:
            print("Error processing captured image:", e)
    else:
        print("Unable to capture the secondary display.")

def main():
    # Call the function to capture and save the image
    get_pic_and_save()

if __name__ == "__main__":
    main()
