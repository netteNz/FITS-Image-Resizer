# FITS Image Resizer

## Overview
The FITS Image Resizer is a Python script that processes FITS image files by cropping them to a specified size and saving them with updated metadata. It allows users to select a source folder, choose a destination folder, and specify crop dimensions.

## Features
- Select source and destination folders using a GUI.
- Crop images from a user-specified upper-left coordinate.
- Save cropped images with updated FITS headers.
- Automatically handles non-compliant FITS headers.
- Ensures valid cropping dimensions to prevent errors.
- **Adjusts World Coordinate System (WCS) values** to maintain correct celestial coordinates.
- **Preserves essential metadata** such as `EXPTIME`, `DATE-OBS`, `FILTER`, `TELESCOP`, and `INSTRUME`.
- **Adds a history entry** to track modifications made to the FITS file.

## Dependencies
Ensure you have the following dependencies installed before running the script:

```sh
pip install astropy numpy tkinter
```

- `astropy`: For handling FITS file operations.
- `numpy`: For efficient numerical operations.
- `tkinter`: For graphical folder selection.

## Usage
1. Run the script:
   ```sh
   python resize.py
   ```
2. Select the **source folder** containing FITS files.
3. Select an **empty destination folder** for cropped images.
4. Enter the cropping parameters:
   - Upper-left X coordinate
   - Upper-left Y coordinate
   - Crop width
   - Crop height
5. The script will process each FITS file in the source folder and save the cropped versions in the destination folder with updated metadata.

## Header Updates
- The FITS header is updated with new image dimensions (`NAXIS1`, `NAXIS2`).
- The **World Coordinate System (WCS) is updated** to reflect the new reference pixel positions (`CRPIX1`, `CRPIX2`).
- Non-compliant FITS headers (invalid values) are automatically handled or removed.
- Essential metadata (`EXPTIME`, `DATE-OBS`, `FILTER`, `TELESCOP`, `INSTRUME`) is preserved.
- A `HISTORY` entry is added to document the modification.

## Error Handling
- If the cropping dimensions exceed the image size, the file will be skipped.
- Non-compliant FITS headers (e.g., invalid values) are automatically handled or removed.
- Ensures that cropped images maintain valid celestial coordinate transformations.

## Example Output
```
Cropped and saved: /destination_folder/cropped_image_01.fits
Cropped and saved: /destination_folder/cropped_image_02.fits
...
```

## License
This project is open-source and available for modification and redistribution under the MIT License.
