# Utility Scripts

This folder contains standalone utility scripts for development and maintenance.

## Available Scripts

### check_images.py

**Purpose:** Scan directories for corrupt or damaged image files.

**Usage:**
```bash
# Check images in current directory
python scripts/check_images.py

# Check images in specific directory
python scripts/check_images.py /path/to/images
```

**Features:**
- Scans for common image formats (.jpg, .jpeg, .png, .bmp, .tiff, .webp)
- Verifies image headers and data integrity
- Reports corrupt files with error details
- Handles interruptions gracefully

**Output:**
```
Scanning directory: ./images for image files...
[CORRUPT] ./images/broken.jpg: image file is truncated

========================================
Scan complete.
Total images checked: 150
Corrupt images found: 1

List of corrupt files:
./images/broken.jpg
```

---

## Note

These scripts are for development/maintenance purposes and are not required for normal operation of dots.ocr.
