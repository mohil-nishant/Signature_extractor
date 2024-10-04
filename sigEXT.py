import cv2
import numpy as np
import os
import pdf2image
from PIL import Image

def crop_signature(image):
    # Convert to grayscale if it's not already
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image

    # Threshold the image to isolate the signature
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Find the largest contour (assuming it's the signature)
        c = max(contours, key=cv2.contourArea)
        
        # Get bounding box
        x, y, w, h = cv2.boundingRect(c)
        
        # Add a small padding
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(gray.shape[1] - x, w + 2*padding)
        h = min(gray.shape[0] - y, h + 2*padding)
        
        # Crop the image
        return image[y:y+h, x:x+w]
    else:
        return image

def extract_signatures(image, output_folder, start_roll):
    # Convert PIL Image to OpenCV format
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to get binary image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours from top-left to bottom-right
    def sort_contours(cnts):
        bounding_boxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, bounding_boxes) = zip(*sorted(zip(cnts, bounding_boxes),
                                             key=lambda b: b[1][1] * 1000 + b[1][0]))
        return cnts
    
    contours = sort_contours(contours)
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Extract and save each signature
    saved_count = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        # Filter out very small contours
        if w > 50 and h > 50:
            # Extract the signature
            signature = image[y:y+h, x:x+w]
            
            # Crop out unnecessary white space
            signature = crop_signature(signature)
            
            # Calculate the roll number
            roll_number = start_roll + saved_count
            
            # Save the signature
            output_path = os.path.join(output_folder, f"roll_{roll_number}.png")
            cv2.imwrite(output_path, signature)
            print(f"Saved signature for roll number {roll_number}")
            
            saved_count += 1
    
    # Return the next roll number to start with
    return start_roll + saved_count

def process_pdf(pdf_path, output_folder, start_roll):
    # Convert PDF to images
    images = pdf2image.convert_from_path(pdf_path)
    
    current_roll = start_roll
    for i, image in enumerate(images):
        print(f"Processing page {i+1}")
        current_roll = extract_signatures(image, output_folder, current_roll)
        print(f"Completed processing page {i+1}")

# Usage
pdf_path = "aaa.pdf"
output_folder = "extracted_signatures"
start_roll_number = 1  # Change this to your starting roll number

process_pdf(pdf_path, output_folder, start_roll_number)