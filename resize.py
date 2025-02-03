#!/usr/bin/env python3
import os
import argparse
import logging
import tkinter as tk
from tkinter import filedialog
from astropy.io import fits
from astropy.wcs import WCS
import numpy as np


def select_folder(title):
    """
    Opens a GUI dialog to select a folder.

    Parameters:
        title (str): Title for the folder selection dialog.

    Returns:
        str: The selected folder path.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory(title=title)
    return folder_path


def crop_fits_images(source_folder, destination_folder, x_start, y_start, x_size, y_size):
    """
    Processes each FITS file in the source folder, crops the image data,
    updates the header (including WCS if available), and saves the new file.

    Parameters:
        source_folder (str): Path to the folder containing original FITS files.
        destination_folder (str): Path to save the cropped FITS files.
        x_start (int): X coordinate of the upper-left corner of the crop.
        y_start (int): Y coordinate of the upper-left corner of the crop.
        x_size (int): Width of the crop.
        y_size (int): Height of the crop.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        logging.info(f"Created destination folder: {destination_folder}")

    for file_name in os.listdir(source_folder):
        if file_name.lower().endswith(".fit"):
            file_path = os.path.join(source_folder, file_name)
            logging.info(f"Processing file: {file_name}")
            try:
                with fits.open(file_path) as hdul:
                    # Look for the first HDU with valid 2D image data
                    image_hdu = None
                    for hdu in hdul:
                        if hdu.data is not None and hdu.data.ndim >= 2:
                            image_hdu = hdu
                            break
                    if image_hdu is None:
                        logging.warning(
                            f"No valid image data found in {file_name}. Skipping.")
                        continue

                    header = image_hdu.header
                    image_data = image_hdu.data

                    # Ensure valid cropping dimensions
                    if (y_start + y_size) > image_data.shape[0] or (x_start + x_size) > image_data.shape[1]:
                        logging.warning(
                            f"Skipping {file_name}: Crop dimensions exceed image size.")
                        continue

                    # Crop the image data
                    cropped_image = image_data[y_start:y_start +
                                               y_size, x_start:x_start + x_size]

                    # Copy header and update new dimensions
                    new_header = header.copy()
                    new_header['NAXIS1'] = x_size
                    new_header['NAXIS2'] = y_size

                    # Update WCS (World Coordinate System) if available
                    if 'CRPIX1' in new_header and 'CRPIX2' in new_header:
                        try:
                            wcs = WCS(header)  # Load WCS from original header
                            # Adjust reference pixel positions
                            wcs.wcs.crpix -= [x_start, y_start]
                            # Apply updated WCS keywords
                            new_header.update(wcs.to_header())
                        except Exception as e:
                            logging.warning(
                                f"Could not update WCS for {file_name}: {e}")

                    # Preserve important metadata
                    metadata_to_keep = ['EXPTIME', 'DATE-OBS',
                                        'FILTER', 'TELESCOP', 'INSTRUME']
                    for key in metadata_to_keep:
                        if key in header:
                            new_header[key] = header[key]

                    # Add a history entry to the header
                    new_header.add_history(
                        f"Cropped to {x_size}x{y_size} pixels at ({x_start}, {y_start})")

                    # Save the cropped FITS file with updated header
                    new_hdul = fits.PrimaryHDU(
                        cropped_image, header=new_header)
                    new_file_path = os.path.join(
                        destination_folder, f"cropped_{file_name}")
                    new_hdul.writeto(
                        new_file_path, overwrite=True, output_verify='fix')
                    logging.info(f"Cropped and saved: {new_file_path}")

            except Exception as e:
                logging.error(f"Error processing {file_name}: {e}")


def main():
    """
    Main function to parse command-line arguments (or prompt via GUI/input)
    and process FITS files.
    """
    parser = argparse.ArgumentParser(
        description="Crop FITS images and update metadata (including WCS)."
    )
    parser.add_argument("--source_folder", type=str,
                        help="Path to source folder containing FITS files.")
    parser.add_argument("--destination_folder", type=str,
                        help="Path to destination folder.")
    parser.add_argument("--x_start", type=int,
                        help="Upper-left corner x-coordinate for cropping.")
    parser.add_argument("--y_start", type=int,
                        help="Upper-left corner y-coordinate for cropping.")
    parser.add_argument("--x_size", type=int, help="Width of crop.")
    parser.add_argument("--y_size", type=int, help="Height of crop.")
    parser.add_argument("--use_gui", action='store_true',
                        help="Use GUI dialogs to select folders even if command-line arguments are provided.")
    args = parser.parse_args()

    # Use GUI folder selection if folder paths are not provided or if forced by --use_gui
    if not args.source_folder or args.use_gui:
        args.source_folder = select_folder(
            "Select Source Folder Containing FITS Files")
    if not args.destination_folder or args.use_gui:
        args.destination_folder = select_folder("Select Destination Folder")

    # Prompt for crop parameters if not provided as command-line arguments
    if args.x_start is None:
        args.x_start = int(input("Enter upper-left corner x-coordinate: "))
    if args.y_start is None:
        args.y_start = int(input("Enter upper-left corner y-coordinate: "))
    if args.x_size is None:
        args.x_size = int(input("Enter width of crop: "))
    if args.y_size is None:
        args.y_size = int(input("Enter height of crop: "))

    # Configure logging to display messages to the console
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s: %(message)s")

    # Process the FITS files
    crop_fits_images(
        args.source_folder,
        args.destination_folder,
        args.x_start,
        args.y_start,
        args.x_size,
        args.y_size
    )


if __name__ == "__main__":
    main()
