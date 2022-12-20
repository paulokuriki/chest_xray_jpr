GAD = ['POS', '+C', 'GD', 'GAD', ' CE', '_CE']
GAD_EXCLUSION = ['SEM', '/S', 'S/', 'PRE']
T1 = ['T1']
T2 = ['T2']
FLAIR = ['FLAIR']
SWI = ['SWI', 'SWAN', 'T2 GRE', 'T2*']
FIESTA = ['FIESTA', 'CISS', 'BALANCE', 'DRIVE']
TOF = ['TOF']
DWI = ['DIF', 'DWI', 'TRACE']
DWI_EXCLUSION = ['ADC', 'APP', 'EXP']
MPR = ['MPR']
ANGIO = ['VEN']
PRIMARY = ['ORIGINAL', 'PRIMARY']
SAG = ['SAG']
AXI = ['AX']
COR = ['COR']
OTHERS = ['3 PL',
          '3-pl',
          'localizer',
          'LOC LOMBAR',
          'Localizador',
          'Localizer',
          'SURVEY',
          'BodyArray',
          'KEY_IMAGES',
          'ADC',
          'MPR',
          'bolus',
          'PJN',
          'Filme'
          ]

TAGS_MR = [
    'PatientID',
    'StudyDescription',
    'SeriesDescription',
    'StudyInstanceUID',
    'SeriesInstanceUID',
    'SOPInstanceUID',
    'ImageType',
    'EchoTime',
    'Primary',
    'RepetitionTime',
    'FlipAngle',
    'SpacingBetweenSlices',
    'SliceThickness',
    'SliceLocation',
    'InstanceNumber',
    'ImageOrientationPatient',
    'Manufacturer',
    'ManufacturerModelName',
    'IOP_Plane',
    'Gad',
    'T2',
    'T1',
    'FLAIR',
    'SWI',
    'DWI',
    'FIESTA',
    'Angio',
    'MPR',
    'Others',
    '000B:0010',
]

TAGS_CT = [
    "AccessionNumber",
    "AcquisitionDate",
    "AcquisitionMatrix",
    "AcquisitionTime",
    "AngioFlag",
    "ConvolutionKernel",
    "ContrastBolusAgent",
    "ImageOrientationPatient",
    "ImagePositionPatient",
    "ImageTime",
    "ImageType",
    "InstitutionName",
    "Manufacturer",
    "ManufacturerModelName",
    "ModalitiesInStudy",
    "Modality",
    "PatientID",
    "ProtocolName",
    "SeriesInstanceUID",
    "SeriesTime",
    "SOPClassUID",
    "SOPInstanceUID",
    "SpacingBetweenSlices",
    "StationName",
    "StudyID",
    "StudyInstanceUID",
    "StudyTime",
    "SliceThickness",
    "SpacingBetweenSlices",
    "StudyDescription",
    "SeriesDescription",
    "IOP_Plane",  # calculates the plane based on ImageOrientationPatient
]

TAGS_CR = [
    "AccessionNumber",
    "AcquisitionDate",
    "ImageType",
    "InstitutionName",
    "Manufacturer",
    "ManufacturerModelName",
    "ModalitiesInStudy",
    "Modality",
    "PatientID",
    "ProtocolName",
    "SeriesInstanceUID",
    "SeriesTime",
    "SOPClassUID",
    "SOPInstanceUID",
    "StationName",
    "StudyID",
    "StudyInstanceUID",
    "StudyTime",
    "StudyDescription",
    "SeriesDescription",
    "ViewPosition",
    "PerformedProtocolCodeSequence",
    "AcquisitionDeviceProcessingDescription",
    "ViewCodeSequence",
    "200B:1011",
    "PixelData"
]
