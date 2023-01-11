from keras.models import load_model
from matplotlib import pyplot
from PIL import Image, ImageOps  # Install pillow instead of PIL
import pandas as pd
import pydicom
from time import sleep
from pydicom.pixel_data_handlers.util import apply_voi_lut
from tqdm.auto import tqdm

tqdm.pandas()
import numpy as np

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

import cv2

# Load the model
model = load_model('./models/classify_thorax.h5', compile=False)

# referente ao cv2:
#  - se der erro ImportError: libGL.so.1: cannot open shared object file: No such file or directory
# -  pode ser necessario instalar:
#      apt-get install libgl1


def read_dicom_img(path: str, voi_lut: bool = True, fix_monochrome: bool = True, resize_x: int = 224,
                   resize_y: int = 224):
    try:
        dicom = pydicom.read_file(path)

        # VOI LUT (if available by DICOM device) is used to transform raw DICOM data to "human-friendly" view
        if voi_lut:
            data = apply_voi_lut(dicom.pixel_array, dicom)
        else:
            data = dicom.pixel_array

        # depending on this value, X-ray may look inverted - fix that:
        if fix_monochrome and dicom.PhotometricInterpretation == "MONOCHROME1":
            data = np.amax(data) - data

        img = data  # - np.min(data)

        img = cv2.resize(img, (resize_x, resize_y), interpolation=cv2.INTER_LANCZOS4)

        img = rescale_0_255(img)

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


def inference_dicom(dicom_file: str):
    predicted_bodypart = None

    array = read_dicom_img(dicom_file)

    if array is not None:

        image = Image.fromarray(array, 'RGB')

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1

        # Load the image into the array
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array

        # run the inference
        prediction = model.predict(data, verbose=0)

        confidence_score = prediction[0][0]

        if confidence_score > 0.5:
            predicted_bodypart = 'Thorax'
        else:
            predicted_bodypart = 'Other'

    return predicted_bodypart


def predict_bodypart(limit_lines: int = None):
    dicomtags_csv = "dicomtags.csv"

    # Reads the CSV containing all dicom tags
    df = pd.read_csv(dicomtags_csv, dtype=str)
    if limit_lines:
        df = df.head(limit_lines)

    print("Running Model 1: Predicting Body Part")
    sleep(0.5)
    df['PredictBodyPart'] = df['Filename'].progress_apply(inference_dicom)

    print("Finished Body Part Prediction")
    print(df['PredictBodyPart'].value_counts())
    # Saves the CSV containing all dicom tags
    df.to_csv(dicomtags_csv, index=False)


# ---------------- OPTIONAL PREVIEWS ------------------
def show_images(df_view):
    for i, row in df_view.iterrows():
        array = read_dicom_img(row['Filename'])

        if array is not None:
            # Load the image into the array
            print('-' * 23 + 'PredictBodyPart: ' + row['PredictBodyPart'] + '-' * 23)
            pyplot.imshow(array)
            pyplot.show()


def show_previews():
    df_view = df[(df['PredictBodyPart'] != 'Thorax')]
    show_images(df_view)

    df_view = df[df['PredictBodyPart'] == 'Thorax'].head(20)
    show_images(df_view)
