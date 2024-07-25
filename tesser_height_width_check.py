import numpy as np
import cv2
import pytesseract
from pytesseract import Output

# Path to Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Otsu's Binarization
    _, binary = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    return binary

def analyze_projection(image):
    vertical_projection = np.sum(image, axis=0)  # Sum of pixel values along columns
    horizontal_projection = np.sum(image, axis=1)  # Sum of pixel values along rows

    # Calculate maximum projection values
    v_max = np.max(vertical_projection)
    h_max = np.max(horizontal_projection)

    return v_max <= h_max

def analyze_images(image_paths):
    results = {}
    for image_path in image_paths:
        pre_image = preprocess_image(image_path)
        is_horizontal = analyze_projection(pre_image)
        results[image_path] = is_horizontal
        print(f"Image: {image_path}, 가로입니까? : {is_horizontal}")

    return results

if __name__ == "__main__":
    # Define the list of image paths
    image_paths = [f'exam/exam{i}.jpg' for i in range(1, 51)]

    # Analyze the images and print results
    results = analyze_images(image_paths)

    # Optionally, you can save the results to a file or perform additional processing
    with open('projection_analysis_results.txt', 'w') as f:
        for image_path, is_horizontal in results.items():
            f.write(f"Image: {image_path}, 가로입니까? : {is_horizontal}\n")
