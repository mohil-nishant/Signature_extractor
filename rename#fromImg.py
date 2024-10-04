import os

def rename_images():
    # Get the current directory
    current_dir = os.getcwd()
    
    # List of common image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')
    
    # Iterate through all files in the current directory
    for filename in os.listdir(current_dir):
        # Check if the file is an image
        if filename.lower().endswith(image_extensions):
            # Remove '#' from the filename
            new_filename = filename.replace('#', '')
            
            # If the filename has changed, rename the file
            if new_filename != filename:
                old_path = os.path.join(current_dir, filename)
                new_path = os.path.join(current_dir, new_filename)
                
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed: {filename} -> {new_filename}")
                except Exception as e:
                    print(f"Error renaming {filename}: {str(e)}")
            else:
                print(f"No change needed for: {filename}")

if __name__ == "__main__":
    rename_images()
    print("Image renaming process complete.")