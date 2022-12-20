import pydicom
from tqdm import tqdm
import pandas as pd
import os
import time
import glob
import numpy as np
from pydicom import _dicom_dict as dc
from constants import *
import string

def dcmtag2df(folder: str, list_of_tags: list):
    """
    # Create a Pandas DataFrame with the <list_of_tags> DICOM tags
    # from the DICOM files in <folder>

    # Parameters:
    #    folder (str): folder to be recursively walked looking for DICOM files.
    #    list_of_tags (list of strings): list of DICOM tags with no whitespaces.


    # Returns:
    #    df (DataFrame): table of DICOM tags from the files in folder.
    """
    list_of_tags = list_of_tags.copy()
    table = []
    start = time.time()

    # checks if folder exists
    if not os.path.isdir(folder):
        print(f'{folder} is not a valid folder.')
        return None

    # joins ** to the folder name for using at the glob function
    print("Searching files recursively...")
    search_folder = os.path.join(folder, '**')

    try:
        filelist = glob.glob(search_folder, recursive=True)
        print(f"{len(list(filelist))} files/folders found ")
    except Exception as e:
        print(e)
        return None
    time.time()
    print("Reading files...")

    for _f in tqdm(filelist):
        try:
            stop_before_pixels = not 'PixelData' in list_of_tags
            dataset = pydicom.dcmread(_f, stop_before_pixels=stop_before_pixels)
            items = []

            items.append(_f)

            for _tag in list_of_tags:
                if _tag in dataset:
                    if dataset.data_element(_tag) is not None:
                        if _tag == 'PixelData':
                            items.append(len(dataset.data_element(_tag).value))
                        else:
                            items.append(str(dataset.data_element(_tag).value))
                    else:
                        if dataset[tag_number] is not None:
                            items.append(str(dataset[tag_number].value))
                        else:
                            items.append("NaN")
                else:
                    series_description = dataset.get('SeriesDescription')
                    if _tag == 'IOP_Plane':
                        IOP = dataset.get('ImageOrientationPatient')
                        _plano = IOP_Plane(IOP)
                        items.append(_plano)
                    elif _tag == "Primary":
                        try:
                            image_type = ' '.join(dataset.get('ImageType'))
                        except:
                            image_type = ''
                        found_word = search_words_in_serie(image_type, PRIMARY)
                        items.append(found_word)
                    elif _tag == "Gad":
                        found_word = search_words_in_serie(series_description, GAD, GAD_EXCLUSION)
                        items.append(found_word)
                    elif _tag == "T1":
                        found_word = search_words_in_serie(series_description, T1, FLAIR + T2)
                        items.append(found_word)
                    elif _tag == "T2":
                        found_word = search_words_in_serie(series_description, T2)
                        items.append(found_word)
                    elif _tag == "FLAIR":
                        found_word = search_words_in_serie(series_description, FLAIR, T1)
                        items.append(found_word)
                    elif _tag == "SWI":
                        found_word = search_words_in_serie(series_description, SWI)
                        items.append(found_word)
                    elif _tag == "FIESTA":
                        found_word = search_words_in_serie(series_description, FIESTA)
                        items.append(found_word)
                    elif _tag == "TOF":
                        found_word = search_words_in_serie(series_description, TOF)
                        items.append(found_word)
                    elif _tag == "DWI":
                        found_word = search_words_in_serie(series_description, DWI, DWI_EXCLUSION)
                        items.append(found_word)
                    elif _tag == "Angio":
                        found_word = search_words_in_serie(series_description, ANGIO)
                        items.append(found_word)
                    elif _tag == "MPR":
                        found_word = search_words_in_serie(series_description, MPR)
                        items.append(found_word)
                    elif _tag == "Others":
                        found_word = search_words_in_serie(series_description, OTHERS)
                        items.append(found_word)
                    else:
                        # checks if a tag number was informed
                        tag_number = tag_number_to_base_16(_tag)
                        if tag_number in dataset:
                            if dataset[tag_number] is not None:
                                items.append(str(dataset[tag_number].value))
                            else:
                                items.append("NaN")
                        else:
                            items.append("NaN")

            table.append((items))
        except (FileNotFoundError, PermissionError):
            pass
        except Exception as e:
            pass

    list_of_tags.insert(0, "Filename")
    test = list(map(list, zip(*table)))
    dictone = {}

    if len(table) == 0:
        print(f'0 DICOM files found at folder: {folder}')
        return None

    for i, _tag in enumerate(list_of_tags):
        dictone[_tag] = test[i]

    df = pd.DataFrame(dictone)
    time.sleep(2)
    print("Finished.")
    return df


def IOP_Plane(IOP: list) -> str:
    """
    This function takes IOP of an image and returns its plane (Sagittal, Coronal, Transverse)
    ['1', '0', '0', '0', '0', '-1'] you are dealing with Coronal plane view
    ['0', '1', '0', '0', '0', '-1'] you are dealing with Sagittal plane view
    ['1', '0', '0', '0', '1', '0'] you are dealing with Axial plane view
    """

    try:
        IOP_round = [round(x) for x in IOP]
        plane = np.cross(IOP_round[0:3], IOP_round[3:6])
        plane = [abs(x) for x in plane]
        if plane[0] == 1:
            return "SAG"
        elif plane[1] == 1:
            return "COR"
        elif plane[2] == 1:
            return "AXI"
        else:
            return "UNK"
    except:
        return "UNK"


def dicomtagnumber_to_tagname(dicom_tag_number: str) -> str:
    # if receives int, convert to str
    dicom_tag_base_16 = tag_number_to_base_16(dicom_tag_number)
    try:
        dicom_tag_name = dc.DicomDictionary.get(dicom_tag_base_16, (0, 0, 0, 0, dicom_tag_number))[4]
        if dicom_tag_name == "0008103E":
            dicom_tag_name = "SeriesDescription"
    except Exception as e:
        print(f'Erro ao converter dicomtag {dicom_tag_number}\n{e}')
    return dicom_tag_name


def dicomtagname_to_tagnumber(dicom_tag_name: str) -> str:
    tag_number_8_digits = dicom_tag_name
    try:
        # searches for Contracted Name
        for key, value in dc.DicomDictionary.items():
            if dicom_tag_name == value[4]:
                tag_number = key
                break
        # searches for Expanded Name if not found Contracted Form
        if not tag_number:
            for key, value in dc.DicomDictionary.items():
                if dicom_tag_name == value[2]:
                    tag_number = key
                    break
        hex_number = hex(1048592)[2:]
        tag_number_8_digits = f"{hex_number:>08}"
    except Exception as e:
        print(f'Erro ao converter dicomtag {dicom_tag_name}\n{e}')
    return tag_number_8_digits


def tag_number_to_base_16(dicom_tag_number: str) -> str:
    # if receives int, convert to str

    hx = string.hexdigits
    if type(dicom_tag_number) == int:
        dicom_tag_number = str(dicom_tag_number)
    only_hexdigits_tag = ''.join(i for i in dicom_tag_number if i in hx)
    dicom_tag_base_16 = int(only_hexdigits_tag, 16)

    return dicom_tag_base_16


def search_words_in_serie(series_description: str, search_words: list, exclusion_words: list = []) -> bool:
    try:
        search_flag = False
        for word in search_words:
            if word.upper() in series_description.upper():
                search_flag = True
                break
    except Exception as e:
        print(f"Erro ao procurar a lista de palavras de inclusao {search_words} na descricao {series_description}")
        return "NaN"

    try:
        exclusion_flag = False
        for word in exclusion_words:
            if word.upper() in series_description.upper():
                exclusion_flag = True
                break
    except Exception as e:
        print(f"Erro ao procurar a lista de palavras de exclusao {search_words} na descricao {series_description}")
        return "NaN"

    found = search_flag and exclusion_flag is False

    return found
