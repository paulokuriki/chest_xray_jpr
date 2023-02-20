import cv2
import matplotlib.pyplot as plt
import os
import numpy as np
from tqdm import tqdm
import zipfile
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
from time import sleep

import pandas as pd

from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

dicomtags_csv = "dicomtags.csv"

png_folder = 'pngs'

anon_zip_file = "anon_images.zip"
anon_csv_file = "anon_exams.csv"

def read_dicom_img(path, voi_lut=True, fix_monochrome=True, resize_x=1024, resize_y=1024):
    try:
        if not os.path.exists(path):
            print(f'File not found: {path}')

        dicom = pydicom.read_file(path)

        # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
        if voi_lut:
            img = apply_voi_lut(dicom.pixel_array, dicom)
        else:
            img = dicom.pixel_array

        # depending on this value, X-ray may look inverted - fix that:
        if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
            img = np.amax(img) - img

        img = img - np.min(img)

        img = cv2.resize(img, (resize_x, resize_y), interpolation=cv2.INTER_LANCZOS4)

        img = rescale_0_1(img)

        img = convert_greyscale_rgb(img)

        return img
    except AttributeError:
        # This file has no image
        pass
    except Exception as e:
        # print(f'Error reading DICOM file: {path}. {e}')
        print(dicom.pixel_array)

    return None


def rescale_0_255(array):
    array_uint8 = np.uint8(255. * (array - np.min(array)) / (np.max(array) - np.min(array)))
    return array_uint8


def rescale_0_1(array):
    array_uint8 = np.float32(1. * (array - np.min(array)) / (np.max(array) - np.min(array)))
    return array_uint8


def convert_greyscale_rgb(array):
    rgb_array = np.stack((array,) * 3, axis=-1)
    return rgb_array

def convert_file(i, dicom_file):

    png_file = os.path.join(png_folder, str(i).zfill(6) + '.png')

    array = read_dicom_img(dicom_file)

    if array is not None:
        f, axarr = plt.subplots(1, 1)

        # axarr.imshow(array, cmap='gray')
        axarr.axis('off')
        plt.imsave(png_file, array, cmap='gray')
        plt.close()
        # plt.show()

        return png_file

    return ""

def convert_png(limit_lines: int = None):


    if not os.path.exists(png_folder):
        os.makedirs(png_folder)

    # Reads the CSV containing all dicom tags
    df = pd.read_csv(dicomtags_csv, dtype=str)
    if limit_lines:
        df = df.head(limit_lines)

    view = 'Frontal'
    bodypart = 'Thorax'

    df = df[(df['PredictedView'] == view) & (df['PredictBodyPart'] == bodypart)]
    df = df.drop_duplicates().reset_index(drop=True)
    df['PNGFilename'] = df.parallel_apply(lambda row: convert_file(row.name, row['Filename']), axis=1)


    print("Converting Selected Images to PNG...")
    sleep(0.5)

    print(f'Zipping PNG anonymized imagens to file {anon_zip_file}')
    png_files = df['PNGFilename'].to_list()
    with zipfile.ZipFile(anon_zip_file, mode="w") as archive:
        for file_path in tqdm(png_files):
            archive.write(file_path)

    print(f'Saving Anonymized CSV file {anon_csv_file}')
    df_anon = df[['ANON_PatientID', 'CalculatedAge', "PatientSex", "PNGFilename"]]
    df_anon.to_csv(anon_csv_file, index=False)

    print("\n\n\nEnd of process!")
    print("\nPlease provide the following files to SPR:")
    print(f'->>> {anon_zip_file}')
    print(f'->>> {anon_csv_file}')


def convert_png_bak(limit_lines: int = None):
    dicomtags_csv = "dicomtags.csv"

    png_folder = 'pngs'

    anon_zip_file = "anon_images.zip"
    anon_csv_file = "anon_exams.csv"

    if not os.path.exists(png_folder):
        os.makedirs(png_folder)

    # Reads the CSV containing all dicom tags
    df = pd.read_csv(dicomtags_csv, dtype=str)
    if limit_lines:
        df = df.head(limit_lines)

    view = 'Frontal'
    bodypart = 'Thorax'

    df = df[(df['PredictedView'] == view) & (df['PredictBodyPart'] == bodypart)]
    df = df.drop_duplicates().reset_index(drop=True)
    df['PNGFilename'] = ""

    print("Converting Selected Images to PNG...")
    sleep(0.5)

    for i, row in tqdm(df.iterrows(), total=len(df)):

        png_file = os.path.join(png_folder, str(i).zfill(6) + '.png')

        dicom_file = row['Filename']
        array = read_dicom_img(dicom_file)

        if array is not None:
            f, axarr = plt.subplots(1, 1)

            # axarr.imshow(array, cmap='gray')
            axarr.axis('off')
            plt.imsave(png_file, array, cmap='gray')
            plt.close()
            # plt.show()

            df.loc[i].at['PNGFilename'] = png_file

    print(f'Zipping PNG anonymized imagens to file {anon_zip_file}')
    png_files = df['PNGFilename'].to_list()
    with zipfile.ZipFile(anon_zip_file, mode="w") as archive:
        for file_path in tqdm(png_files):
            archive.write(file_path)

    print(f'Saving Anonymized CSV file {anon_csv_file}')
    df_anon = df[['ANON_PatientID', 'CalculatedAge', "PatientSex", "PNGFilename"]]
    df_anon.to_csv(anon_csv_file, index=False)

    print("\n\n\nEnd of process!")
    print("\nPlease provide the following files to SPR:")
    print(f'->>> {anon_zip_file}')
    print(f'->>> {anon_csv_file}')
