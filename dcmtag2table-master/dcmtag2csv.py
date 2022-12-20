import os
import tempfile as tmp
from aux_lib import dcmtag2df
from constants import *

# list of tags to export do csv
list_of_tags = TAGS_CR

#folder = os.getcwd()

folder = "../dicom_files"
export_csv = "dicomtags.csv"
export_csv = os.path.join(folder, export_csv)

df = dcmtag2df(folder, list_of_tags)

try:
    if len(df.index) > 0:
        df.to_csv(export_csv, index=False)
        print(f'{export_csv} exported successfully.')
    else:
        print(f'{export_csv} not modified.')
except PermissionError:
    new_filename = os.path.join(folder, next(tmp._get_candidate_names()) + ".csv")
    df.to_csv(new_filename, index=False)
    print(f'{export_csv} was locked. New file exported to the filename {new_filename} successfully.')
except Exception as e:
    print(f'Error exporting {export_csv} file.\n' + str(e))