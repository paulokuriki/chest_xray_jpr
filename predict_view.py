import os
from keras.models import load_model
from matplotlib import pyplot
import pandas as pd
from time import sleep

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut

from tqdm.auto import tqdm

tqdm.pandas()

import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

import cv2

# Load the model
model = load_model('./models/predict_view.h5', compile=False)



# - referente ao cv2:
# - se der erro ImportError: libGL.so.1: cannot open shared object file: No such file or directory
# -  pode ser necessario instalar:
# --->>>  apt-get install libgl1

def read_dicom_img(path, voi_lut=True, fix_monochrome=True, resize_x=200, resize_y=200):
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


def predict_view(dicom_file):
    confidence_score = np.nan

    try:
        array = read_dicom_img(dicom_file)

        if array is not None:

            array = array.astype(np.float32)

            # Load the image into the array
            data = np.ndarray(shape=(1, 200, 200, 3), dtype=np.float32)
            data[0] = array

            # pyplot.imshow(array)
            # pyplot.show()

            # run the inference
            prediction = model.predict(data, verbose=0)

            pred = prediction[0][0]
            if pred < 0.2:
                return 'Frontal'
            else:
                return 'Lateral'
    except Exception as e:
        pass
        # print(e)

    return np.nan


def predict_xray_view(limit_lines: int = None):
    dicomtags_csv = "dicomtags.csv"


    # Reads the CSV containing all dicom tags
    df = pd.read_csv(dicomtags_csv, dtype=str)
    if limit_lines:
        df = df.head(limit_lines)

    print("Running Model 2: Predicting Chest View")
    sleep(0.5)
    df['PredictedView'] = df['Filename'].progress_apply(predict_view)

    print("Finished View Prediction")
    print(df['PredictedView'].value_counts())
    # Saves the CSV containing all dicom tags
    df.to_csv(dicomtags_csv, index=False)


# ---------------- OPTIONAL PREVIEWS ------------------
def show_images(df):
    for i, row in df.iterrows():
        array = read_dicom_img(row['Filename'])

        if array is not None:
            # Load the image into the array
            print('-' * 23 + row['PredictedView'].upper() + '-' * 23)
            pyplot.imshow(array)
            pyplot.show()


def show_previews():
    view = 'Frontal'
    df_view = df[df['PredictedView'] == view].head(20)
    show_images(df_view)

    view = 'Lateral'
    df_view = df[df['PredictedView'] == view].head(20)
    show_images(df_view)
