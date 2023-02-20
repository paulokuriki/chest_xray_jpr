from aux_lib import dcmtag2df, save_csv
from constants import *
from datetime import datetime
from dateutil import relativedelta
import numpy as np

import random
random.seed(datetime.now().timestamp())

import warnings
warnings.filterwarnings("ignore")

# list of tags to export do csv
list_of_tags = TAGS_CR

def read_dicom_tags(dicom_folder: str, institution_prefix: str, export_csv = "dicomtags.csv"):

    # reads dicom dicom files and store metadata in a dataframe
    df = dcmtag2df(dicom_folder, list_of_tags)

    # calculates age
    def calculate_age(birth_date: str, exam_datetime: str) -> int:
        try:
            if birth_date is not np.nan and birth_date not in ['', 'NaN'] and  exam_datetime is not np.nan and exam_datetime not in ['', 'NaN']:
                date_pattern = "%Y%m%d"
                start_date = datetime.strptime(birth_date, date_pattern)

                date_pattern = "%Y%m%d"
                end_date = datetime.strptime(exam_datetime, date_pattern)

                # Get the relativedelta between two dates
                delta = relativedelta.relativedelta(end_date, start_date)

                return delta.years
            else:
                return np.nan
        except Exception as e:
            return np.nan

        return np.nan

    df['CalculatedAge'] = df.apply(lambda row: calculate_age(row['PatientBirthDate'], row['StudyDate']), axis=1)

    # selects only ages between 18 and 99 years
    df = df[(df['CalculatedAge'] >= 18) & (df['CalculatedAge'] <= 99)]

    # gets a list of unique patient ids and shuffles
    patient_ids = list(set(df['PatientID'].to_list()))
    random.shuffle(patient_ids)

    # creates an ordered dictionary based on the suffled list of unique pat ids
    dict_anon_pat_id = {v:str(i).zfill(8) for i, v in enumerate(patient_ids)}

    # creates a new field based on the dict
    df['ANON_PatientID'] = df.apply(lambda row: institution_prefix + '_' + dict_anon_pat_id.get(row['PatientID']), axis=1)

    # saves metadata to a csv
    save_csv(df, export_csv)



