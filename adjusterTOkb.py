import os
from PIL import Image
import io

def make_image_10kb(input_path, output_path):
    target_size = 55 * 1024  # 10 KB in bytes
    
    with Image.open(input_path) as img:
        # Convert to RGB if the image is in RGBA mode
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        # Start with a high quality
        quality = 95
        
        while True:
            # Save the image to a buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=quality)
            size = buffer.tell()
            
            if size == target_size:
                # If we hit exactly 10 KB, save and exit
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                break
            elif size < target_size:
                # If the image is smaller than 10 KB, pad it
                with open(output_path, 'wb') as f:
                    f.write(buffer.getvalue())
                    f.write(b'\0' * (target_size - size))
                break
            else:
                # If the image is larger than 10 KB, reduce quality and try again
                quality -= 1
                if quality < 1:
                    # If we can't reduce quality further, truncate to 10 KB
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue()[:target_size])
                    break

    print(f"Adjusted image saved: {output_path}")

def process_directory():
    current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, "10kb_images")
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(current_dir):
        if filename.lower().endswith('.png'):
            input_path = os.path.join(current_dir, filename)
            output_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.jpg')
            make_image_10kb(input_path, output_path)

if __name__ == "__main__":
    process_directory()
    print("Processing complete. 10 KB images are in the '10kb_images' directory.")