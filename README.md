# FITS Image Resizer

## Overview
Python script that processes FITS image files by cropping them to a specified size and saving them with preserved metadata. It allows selection of a source folder, a destination folder, and specify crop dimensions.

## Features
- Select source and destination folders using a GUI.
- Crop images from a user-specified upper-left coordinate.
- Save cropped images with their original FITS headers.
- Automatically handles non-compliant FITS headers.
- Ensures valid cropping dimensions to prevent errors.

## Dependencies

```sh
pip install astropy numpy tkinter
```

- `astropy`: For handling FITS file operations.
- `numpy`: For numerical operations.
- `tkinter`: For graphical folder selection.

## Usage
1. Run the script:
   ```sh
   python fits_resizer.py
   ```
2. Select the **source folder** containing FITS files.
3. Select an **empty destination folder** for cropped images.
4. Enter the cropping parameters:
   - Upper-left X coordinate
   - Upper-left Y coordinate
   - Crop width
   - Crop height
5. The script will process each FITS file in the source folder and save the cropped versions in the destination folder.

## Error Handling
- If the cropping dimensions exceed the image size, the file will be skipped.
- Non-compliant FITS headers (e.g., invalid values) are automatically handled or removed.

## Example Output
```
Cropped and saved: /destination_folder/cropped_image_01.fits
Cropped and saved: /destination_folder/cropped_image_02.fits
...
```

## License
This project is open-source and available for modification and redistribution under the MIT License.

