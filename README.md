# SPR Chest X-Ray Challenge. 
## Dataset Provider Module

### Usage: python process.py [-h] -f DICOM_FOLDER -i INSTITUTION [-l LIMIT]

### Options:

-h, --help            show this help message and exit

-f DICOM_FOLDER, --folder DICOM_FOLDER
                        Folder containing the DICOM files. It will be read
                        recursively.

-i INSTITUTION        Institution Sufix. Eg. DASA, UNIFESP, HC-USP, HIAE,
                        SIRIO, FLEURY

-l LIMIT              [Optional] Limit of files processed. Used only for testing
                        purpose.

E.g.: python process.py -f dicom_folder -i DASA -l 100
      
Process only 100 cases for testing purpose
      
      
E.g.: python process.py -f dicom_folder -i DASA 
      
To process all DICOM files, supress the -l parameter
      
      
At the end of the process, the following files should be submitted to SPR bucket:
- anon_exams.csv
- anon_images.zio
