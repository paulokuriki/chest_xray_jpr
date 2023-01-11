from argparse import ArgumentParser

from read_dicom_tags import read_dicom_tags
from predict_bodypart import predict_bodypart
from predict_view import predict_xray_view
from convert_png import convert_png

parser = ArgumentParser(description='SPR Chest X=Ray Challenge. Dataset Provider Module')

parser.add_argument('-f',  '--folder', action='store', dest='dicom_folder', required=True,
                    help='Folder containing the DICOM files. It will be read recursively.')
parser.add_argument('-i', action='store', dest='institution', required=True,
                    help='Institution Sufix. Eg. DASA, UNIFESP, HC-USP, HIAE, SIRIO, FLEURY')
parser.add_argument('-l', action='store', dest='limit', required=False, type=int,
                    help='Limit of files processed. Used only for testing purpose.')

args = parser.parse_args()
institution_prefix = args.institution
dicom_folder = args.dicom_folder
if args.limit:
    limit_lines = int(args.limit)

read_dicom_tags(dicom_folder, institution_prefix)

predict_bodypart(limit_lines)

predict_xray_view(limit_lines)

convert_png(limit_lines)
