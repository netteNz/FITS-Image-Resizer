Below is a simple `README.md` that you can include with your script:

---

# FITS Crop Script

This script crops FITS images while preserving important metadata—including updating the World Coordinate System (WCS) information in the FITS header. It is useful for batch processing astronomical images when you need to extract a region of interest.

## Features

- **Batch Processing:** Processes all FITS files in a specified source folder.
- **Accurate Cropping:** Uses user-defined starting coordinates and dimensions (width and height in pixels) to crop images.
- **Metadata Preservation:** Updates the FITS header with the new image dimensions and preserves key metadata (e.g., `EXPTIME`, `DATE-OBS`, `FILTER`, `TELESCOP`, `INSTRUME`).
- **WCS Adjustment:** Automatically updates the WCS reference pixel values (`CRPIX1` and `CRPIX2`) if present.
- **Multi-HDU Support:** Finds the first HDU containing valid 2D image data.
- **Command-Line & GUI Options:** Accepts crop parameters via command-line arguments, or falls back to GUI dialogs (using Tkinter) and console input.
- **Logging:** Uses Python’s `logging` module to output information and error messages.

## Requirements

- Python 3.x
- [Astropy](https://www.astropy.org/)
- [NumPy](https://numpy.org/)
- Tkinter

Install the required Python packages (if not already installed) via pip:

```bash
pip install astropy numpy
```

## Usage
The script is mainly designed for a user-friendly GUI workflow:
 - **Folder Selection:**  
A Tkinter dialog lets you choose the source folder (with FITS files) and the destination folder (for saving cropped images).
- **Crop Parameters:**  
You are prompted via the console to enter:
    - `x_start` and `y_start`: The 0-indexed pixel coordinates of the upper-left corner of the crop.
    - `x_size` and `y_size`: The width and height (in pixels) of the crop.
- **Alternative Usage (Command-Line Mode):**  
  For more advanced or automated workflows, you can provide parameters via command-line arguments. The following commands are available:
  **Basic Command-Line Example:**
    ```bash
    python resize.py --source_folder /path/to/source \
                        --destination_folder /path/to/destination \
                        --x_start 100 --y_start 100 \
                        --x_size 500 --y_size 500
    ```

## Script Details

- **Source Folder:** The directory containing your original FITS files.
- **Destination Folder:** The directory where cropped FITS files will be saved.
- **x_start & y_start:** The 0-indexed pixel coordinates (in your Python array) marking the upper-left corner of the crop.
- **x_size & y_size:** The width and height (in pixels) of the crop. For example, an `x_size` of 300 means the cropped image will include 300 pixels in the horizontal direction.
- **WCS Update:** If the FITS header includes WCS keywords (like `CRPIX1` and `CRPIX2`), the script adjusts these values to reflect the crop. Note that while FITS headers use 1-indexed coordinates, the cropping uses 0-indexed pixel positions in the Python array.


## Logging

The script logs progress and errors to the console using Python’s `logging` module. This helps you track which files were processed, skipped, or encountered errors.
