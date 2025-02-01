import os
import tkinter as tk
from tkinter import filedialog
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np

def select_folder(title):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title=title)
    return folder_path

def crop_fits_images(source_folder, destination_folder, x_start, y_start, x_size, y_size):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    for file_name in os.listdir(source_folder):
        if file_name.endswith(".fits"):
            file_path = os.path.join(source_folder, file_name)

            with fits.open(file_path) as hdul:
                header = hdul[0].header
                image_data = hdul[0].data

                # Ensure valid cropping dimensions
                if (y_start + y_size) > image_data.shape[0] or (x_start + x_size) > image_data.shape[1]:
                    print(f"Skipping {file_name}: Crop dimensions exceed image size.")
                    continue

                # Crop the image
                cropped_image = image_data[y_start:y_start + y_size, x_start:x_start + x_size]

                # Update Header with New Dimensions
                new_header = header.copy()
                new_header['NAXIS1'] = x_size
                new_header['NAXIS2'] = y_size

                # Update WCS (World Coordinate System)
                if 'CRPIX1' in new_header and 'CRPIX2' in new_header:
                    wcs = WCS(header)  # Load WCS from original header
                    wcs.wcs.crpix -= [x_start, y_start]  # Adjust reference pixel positions
                    new_header.update(wcs.to_header())  # Apply updated WCS

                # Preserve important metadata
                metadata_to_keep = ['EXPTIME', 'DATE-OBS', 'FILTER', 'TELESCOP', 'INSTRUME']
                for key in metadata_to_keep:
                    if key in header:
                        new_header[key] = header[key]

                # Add a history entry
                new_header.add_history(f"Cropped to {x_size}x{y_size} pixels at ({x_start}, {y_start})")

                # Save cropped FITS with updated header
                new_hdul = fits.PrimaryHDU(cropped_image, header=new_header)
                new_file_path = os.path.join(destination_folder, f"cropped_{file_name}")
                new_hdul.writeto(new_file_path, overwrite=True, output_verify='silentfix')

                print(f"Cropped and saved: {new_file_path}")

if __name__ == "__main__":
    # Select Source and Destination Folders
    source_folder = select_folder("Select Source Folder Containing FITS Files")
    destination_folder = select_folder("Select Destination Folder")

    # User Input: Crop Parameters
    x_start = int(input("Enter upper-left corner x-coordinate: "))
    y_start = int(input("Enter upper-left corner y-coordinate: "))
    x_size = int(input("Enter width of crop: "))
    y_size = int(input("Enter height of crop: "))

    # Process FITS Files
    crop_fits_images(source_folder, destination_folder, x_start, y_start, x_size, y_size)
