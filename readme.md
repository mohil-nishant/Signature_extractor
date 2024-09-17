# Signature Extractor

## Description
Signature Extractor is a Python script designed to extract individual signatures from a PDF document containing multiple signed rectangles. It's particularly useful for processing large batches of signatures, such as those collected for academic or administrative purposes.

## Features
- Extracts signatures from PDF files
- Handles multiple pages
- Automatically detects signature boxes (white rectangles with black outlines)
- Crops unnecessary white space around signatures
- Saves each signature as an individual image file
- Names files sequentially based on a starting roll number

## Requirements
- Python 3.6+
- OpenCV (`cv2`)
- NumPy
- pdf2image
- Pillow (PIL)
- poppler (required by pdf2image)

## Installation

1. Clone this repository:

2. Install the required Python packages:
   ```
   pip install opencv-python numpy pdf2image pillow
   ```

3. Install poppler:
   - On Windows: Download from [poppler for Windows](http://blog.alivate.com.au/poppler-windows/) and add the `bin` folder to your system PATH.
   - On macOS: `brew install poppler`
   - On Linux: `sudo apt-get install poppler-utils` (Ubuntu/Debian) or use your distribution's package manager.

## Usage

1. Place your PDF file containing signatures in a known location.

2. Open the `signature_extractor.py` file and update the following variables:
   - `pdf_path`: Set to the path of your PDF file.
   - `output_folder`: Set to the folder where you want to save the extracted signatures.
   - `start_roll_number`: Set to the starting roll number for naming the signature files.

3. Run the script:
   ```
   python signature_extractor.py
   ```

4. The script will process the PDF and save individual signature images in the specified output folder.

## Output

The script generates PNG image files for each extracted signature. Files are named in the format `roll_X.png`, where X is the roll number starting from `start_roll_number`.

## Troubleshooting

If you encounter issues with signature detection or extraction:
- Ensure your PDF is of good quality and the signature boxes are clearly visible.
- Adjust the threshold values in the script if needed (in the `extract_signatures` and `crop_signature` functions).
- Check that poppler is correctly installed and accessible in your system PATH.

## Acknowledgements

- OpenCV community for their excellent computer vision library
- pdf2image developers for making PDF processing easier in Python
