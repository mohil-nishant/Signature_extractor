import os
from PIL import Image

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

def process_directory(crop_pixels=10):
    # Get the current directory
    current_dir = os.getcwd()
    
    # Create a new directory for cropped images
    output_dir = os.path.join(current_dir, "cropped_images")
    os.makedirs(output_dir, exist_ok=True)
    
    # List all files in the current directory
    for filename in os.listdir(current_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(current_dir, filename)
            output_path = os.path.join(output_dir, filename)
            crop_image(input_path, output_path, crop_pixels)

if __name__ == "__main__":
    process_directory()
    print("Processing complete. Cropped images are in the 'cropped_images' directory.")