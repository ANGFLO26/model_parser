import os
import sys
from PIL import Image, ImageFile

# Configure PIL to handle truncated images to check if they are readable, 
# but we want to detecting them, so we keep default behavior or catch exceptions.
# By default PIL raises IOError for truncated images.

def check_images(directory):
    corrupt_files = []
    checked_count = 0
    
    print(f"Scanning directory: {directory} for image files...")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp')):
                file_path = os.path.join(root, file)
                checked_count += 1
                
                try:
                    # Attempt to open and verify the image
                    with Image.open(file_path) as img:
                        img.verify() # Fast check of header consistency
                        
                    # Also try to load the data to catch "premature end of data"
                    # verify() doesn't read the whole file, but load() does.
                    # We need to re-open because verify() consumes the file pointer structure
                    with Image.open(file_path) as img:
                        img.load()
                        
                except (OSError, SyntaxError, Exception) as e:
                    print(f"[CORRUPT] {file_path}: {e}")
                    corrupt_files.append(file_path)
                except KeyboardInterrupt:
                    print("\nScan interrupted by user.")
                    return

    print("\n" + "="*40)
    print(f"Scan complete.")
    print(f"Total images checked: {checked_count}")
    print(f"Corrupt images found: {len(corrupt_files)}")
    
    if corrupt_files:
        print("\nList of corrupt files:")
        for f in corrupt_files:
            print(f)
        
        print("\nTo remove these files, you can delete them manually.")
    else:
        print("\nNo corrupt images found.")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    check_images(target_dir)
