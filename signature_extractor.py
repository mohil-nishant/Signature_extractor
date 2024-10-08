import cv2
import numpy as np
import os
import pdf2image
from PIL import Image
import io

def crop_signature(image):
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)
        padding = 5
        x = max(0, x - padding)
        y = max(0, y - padding)
        w = min(gray.shape[1] - x, w + 2*padding)
        h = min(gray.shape[0] - y, h + 2*padding)
        return image[y:y+h, x:x+w]
    else:
        return image

def extract_signatures(image, output_folder, start_roll):
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    def sort_contours(cnts):
        bounding_boxes = [cv2.boundingRect(c) for c in cnts]
        (cnts, bounding_boxes) = zip(*sorted(zip(cnts, bounding_boxes),
                                             key=lambda b: b[1][1] * 1000 + b[1][0]))
        return cnts
    
    contours = sort_contours(contours)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    saved_count = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:
            signature = image[y:y+h, x:x+w]
            signature = crop_signature(signature)
            roll_number = start_roll + saved_count
            output_path = os.path.join(output_folder, f"roll_{roll_number}.png")
            cv2.imwrite(output_path, signature)
            print(f"Saved signature for roll number {roll_number}")
            saved_count += 1
    
    return start_roll + saved_count

def process_pdf(pdf_path, output_folder, start_roll):
    images = pdf2image.convert_from_path(pdf_path)
    current_roll = start_roll
    for i, image in enumerate(images):
        print(f"Processing page {i+1}")
        current_roll = extract_signatures(image, output_folder, current_roll)
        print(f"Completed processing page {i+1}")

def crop_image(input_path, output_path, crop_pixels=20):
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            crop_box = (crop_pixels, crop_pixels, width - crop_pixels, height - crop_pixels)
            cropped_img = img.crop(crop_box)
            cropped_img.save(output_path)
            print(f"Cropped image saved: {output_path}")
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")

def make_image_10kb(input_path, output_path):
    target_size = 11 * 1024  # 11 KB in bytes
    with Image.open(input_path) as img:
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        quality = 95
        while True:
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            size = buffer.tell()
            if size <= target_size:
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                    if size < target_size:
                        f.write(b'\0' * (target_size - size))
                break
            quality -= 1
            if quality < 1:
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue()[:target_size])
                break
    print(f"Adjusted image saved: {output_path}")

def main():
    # Step 1: Process PDF and extract signatures
    pdf_path = "aaaa.pdf"
    signatures_folder = "extracted_signatures"
    start_roll_number = 1
    process_pdf(pdf_path, signatures_folder, start_roll_number)

    # Step 2: Crop extracted signatures
    cropped_folder = "cropped_images"
    os.makedirs(cropped_folder, exist_ok=True)
    for filename in os.listdir(signatures_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(signatures_folder, filename)
            output_path = os.path.join(cropped_folder, filename)
            crop_image(input_path, output_path, crop_pixels=10)

    # Step 3: Resize cropped images to 11 KB
    final_folder = "11kb_images"
    os.makedirs(final_folder, exist_ok=True)
    for filename in os.listdir(cropped_folder):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(cropped_folder, filename)
            output_path = os.path.join(final_folder, os.path.splitext(filename)[0] + '.jpg')
            make_image_10kb(input_path, output_path)

    print("All processing complete. Final images are in the '11kb_images' directory.")

if __name__ == "__main__":
    main()
