import os
from PIL import Image
import io

def make_image_10kb(input_path, output_path):
    target_size = 13 * 1024  # 10 KB in bytes
    
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if the image is not in RGB mode
            if img.mode not in ['RGB', 'L']:
                img = img.convert('RGB')
            
            # Start with a high quality
            quality = 95
            
            while True:
                # Save the image to a buffer
                buffer = io.BytesIO()
                
                # Determine output format based on file extension
                output_format = os.path.splitext(output_path)[1][1:].upper()
                if output_format not in ['JPEG', 'JPG', 'PNG', 'BMP', 'WEBP']:
                    output_format = 'JPEG'  # Default to JPEG if format not supported
                
                # Save with format-specific parameters
                if output_format in ['JPEG', 'JPG']:
                    img.save(buffer, format='JPEG', quality=quality)
                elif output_format == 'PNG':
                    img.save(buffer, format='PNG', optimize=True)
                elif output_format == 'WEBP':
                    img.save(buffer, format='WEBP', quality=quality)
                elif output_format == 'BMP':
                    img.save(buffer, format='BMP')
                
                size = buffer.tell()
                
                if size <= target_size:
                    # If the image is smaller than or equal to 10 KB, pad it if needed
                    with open(output_path, 'wb') as f:
                        f.write(buffer.getvalue())
                        if size < target_size:
                            f.write(b'\0' * (target_size - size))
                    break
                else:
                    # If the image is larger than 10 KB, reduce quality and try again
                    quality -= 5  # Decrease by larger steps for faster processing
                    if quality < 1:
                        # If we can't reduce quality further, truncate to 10 KB
                        with open(output_path, 'wb') as f:
                            f.write(buffer.getvalue()[:target_size])
                        break
        
        print(f"Successfully processed: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return False

def process_directory(input_dir=None, output_dir=None, output_format='jpg'):
    """
    Process all supported image files in a directory.
    
    Args:
        input_dir (str): Input directory path. Defaults to current directory.
        output_dir (str): Output directory path. Defaults to '10kb_images' in current directory.
        output_format (str): Desired output format ('jpg', 'png', 'webp', 'bmp'). Defaults to 'jpg'.
    """
    # Set up directories
    input_dir = input_dir or os.getcwd()
    output_dir = output_dir or os.path.join(input_dir, "10kb_images")
    os.makedirs(output_dir, exist_ok=True)
    
    # Supported input formats
    supported_formats = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff'}
    
    # Process files
    processed_count = 0
    error_count = 0
    
    for filename in os.listdir(input_dir):
        file_ext = os.path.splitext(filename)[1].lower()
        if file_ext in supported_formats:
            input_path = os.path.join(input_dir, filename)
            output_filename = f"{os.path.splitext(filename)[0]}.{output_format}"
            output_path = os.path.join(output_dir, output_filename)
            
            if make_image_10kb(input_path, output_path):
                processed_count += 1
            else:
                error_count += 1
    
    print(f"\nProcessing complete:")
    print(f"- Successfully processed: {processed_count} images")
    print(f"- Errors encountered: {error_count} images")
    print(f"- Output directory: {output_dir}")

if __name__ == "__main__":
    # Example usage with custom parameters
    process_directory(output_format='jpg')
