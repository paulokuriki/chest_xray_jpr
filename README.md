# SPR Chest X-Ray Challenge. 
## Dataset Provider Module

### Usage: process.py [-h] -f DICOM_FOLDER -i INSTITUTION [-l LIMIT]

### Options:

-h, --help            show this help message and exit

-f DICOM_FOLDER, --folder DICOM_FOLDER
                        Folder containing the DICOM files. It will be read
                        recursively.

-i INSTITUTION        Institution Sufix. Eg. DASA, UNIFESP, HC-USP, HIAE,
                        SIRIO, FLEURY

-l LIMIT              Limit of files processed. Used only for testing
                        purpose.

E.g.: python -f dicom_folder -i DASA -l 100
      Process only 10 cases for testing purpose
      
      
E.g.: python -f dicom_folder -i DASA 
      To process all DICOM files, supress the -l parameter
      
      
The following files should be submitted to SPR bucket:
- anon_exams.csv
- anon_images.zio