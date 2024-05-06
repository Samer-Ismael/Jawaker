# Jawaker
This Python project is a card detection system designed to recognize playing cards from a secondary display or image input.

## Overview

The project utilizes computer vision techniques to capture and process images, comparing them with preloaded card images to identify and detect playing cards. It includes functionalities to:

- Capture screenshots from a secondary display.
- Process and crop captured images.
- Detect and recognize playing cards from the captured images.
- Provide real-time feedback on the detected cards.

## Dependencies

The following dependencies are required to run the project:

- Python 3.8 or higher
- OpenCV
- NumPy
- Pillow
- MSS (Multi-Screen Shot)
- scikit-image

These dependencies can be installed via the `requirements.txt` file using the following command:

```bash
pip install -r requirements.txt
```

## Usage

To use the card detection system:

1. Ensure that Python and the required dependencies are installed on your system.
2. Clone or download the project repository.
3. Navigate to the project directory.

### Running the Application

Run the `service.py` script to start the Flask web server, which serves as the backend for the card detection system:

```bash
python main.py
```

Once the server is running, you can access the detected cards data via the endpoint:

```
http://localhost:5000/cards
```

The detected cards will be returned as a JSON list.

### Customization

- Adjust the similarity threshold in the `compare_images` method to fine-tune card detection accuracy.
- Modify the cropping parameters in the `get_pic_and_save` method to adjust the portion of the screen captured and processed.

To customize the portion of the screen being watched by the application, follow these steps:

1. Open the `get_pic_and_save` method in the `CardDetector` class.
2. Locate the following lines of code:

    ```python
    top_percentage_to_remove = 0.08
    crop_top_percentage = 0  # Adjust this value to change the top cropping percentage
    crop_right_percentage = 0  # Adjust this value to change the right cropping percentage
    ```

3. Adjust the values of `crop_top_percentage` and `crop_right_percentage` variables to specify the desired top and right cropping percentages, respectively.
4. Experiment with different percentage values to capture the desired part of the screen.
5. Save the changes and run the application to see the updated captured area.

Feel free to adjust these parameters as needed to fit your specific use case!

Feel free to adjust these parameters as needed to fit your specific use case!

## License

This project is licensed under the [MIT License](LICENSE).