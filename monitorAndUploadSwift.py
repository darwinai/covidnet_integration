### This script is supposed to be used in the following folder structure:
### using hospitalSystemA for example, starting from level 1
### level 1: hospitalSystemA
### level 2: Hospital1 Hospital2 .... covidnet_integration
### similarly for other hospital systems 
### to run: python3 monitorAndUploadSwift.py

import swiftclient
import time
import argparse

from pydicom import dcmread
import os
from os import listdir, system, environ
from os.path import isfile, join

from chrisclient import client

TIME_TO_WAIT_BEFORE_NEXT_UPLOAD = 3600

chris_client = client.Client("http://localhost:8000/api/v1/", "chris", "chris1234")

# Swift service settings
DEFAULT_FILE_STORAGE = 'swift.storage.SwiftStorage'
SWIFT_AUTH_URL = 'http://127.0.0.1:8080/auth/v1.0'
SWIFT_USERNAME = 'chris:chris1234'
SWIFT_KEY = 'testing'
SWIFT_CONTAINER_NAME = 'users'
output_path = 'SERVICES/PACS/covidnet'

# folders for each hospital system
hospital_system_folders = {
    'hospitalSystemA':[
        "Hospital1",
        "Hospital2",
        "Hospital3"
    ],
    'hospitalSystemB': [
        "Hospital1",
        "Hospital2",
    ],
    'hospitalSystemC': [
        "Hospital1",
    ]
}

def UploadSwift(folder: str, dcmFiles):
    # uploads all the files in a folder to swift

    for f in dcmFiles:
        system(f'swift -A {SWIFT_AUTH_URL} -U {SWIFT_USERNAME} '
        + '-K testing upload users {}/{} '.format(f[0], f[1]) 
        +'--object-name "{}/{}"'.format(output_path, f[1]))

    # initiate a Swift service connection
    conn = swiftclient.Connection(user=SWIFT_USERNAME,
                                key=SWIFT_KEY,
                                authurl=SWIFT_AUTH_URL)
    object_list = []
    poll_loop = 0
    max_polls = 20

    while len(object_list) < len(dcmFiles) and poll_loop < max_polls:
        object_list = conn.get_container(
                    SWIFT_CONTAINER_NAME, 
                    prefix=output_path,
                    full_listing=True)[1]
        if len(object_list) < len(dcmFiles):
            time.sleep(0.2)
            poll_loop += 1

    # notify Cube
    for index in range(len(dcmFiles)):
        f = dcmFiles[index]
        with open(join(f[0],f[1]), 'rb') as infile:
            ds = dcmread(infile)
            fileName = f[1]
            pacs_data = {
                'path': f'SERVICES/PACS/covidnet/{fileName}', 
                'PatientID': str(ds.PatientID) if hasattr(ds, 'PatientBirthDate') and ds.PatientID else '11111111',  
                'PatientName': str(ds.PatientName), 
                'PatientBirthDate': str(ds.PatientBirthDate) if hasattr(ds, 'PatientBirthDate') and ds.PatientBirthDate != '' else '1970-12-31',
                'PatientAge': str(ds.PatientAge) if hasattr(ds, 'PatientAge') else '50',
                'PatientSex': str(ds.PatientSex) if hasattr(ds, 'PatientSex') else '',
                'StudyInstanceUID': str(ds.StudyInstanceUID) if hasattr(ds, 'StudyInstanceUID') else '99999999',
                'StudyDescription':  str(ds.StudyDescription) if hasattr(ds, 'StudyDescription') else 'Default Study Description', 
                'SeriesInstanceUID': str(ds.SeriesInstanceUID), 
                'SeriesDescription': str(ds.SeriesDescription) if hasattr(ds, 'SeriesDescription') else 'Default Description', 
                'Modality': ds.Modality if hasattr(ds, 'Modality') else 'CR',
                'pacs_name': 'covidnet'
            }
            try:
                print('Uploading: ', pacs_data)
                chris_client.register_pacs_file(pacs_data)
            except Exception as e:
                print(f'{f[1]} error: {str(e)}')
                continue
            print('SUCCESS')
            


def getCurrentHomeFolderAbsolute():
    currentDirectory = os.getcwd().split('/')
    currentDirectory.pop()
    return '/'.join(currentDirectory) 


if __name__== "__main__":
    current_directory = getCurrentHomeFolderAbsolute()
    hospital_system = current_directory.split('/').pop()
    folders = hospital_system_folders[hospital_system]
    # create a set to store uploaded images for each hospital subfolder
    hospitals_dict = {}
    for folder in folders:
        hospitals_dict[folder] = set()
    
    while True:
        for folder in folders:
            existing_images = hospitals_dict[folder]
            folderName = f"{current_directory}/{folder}"

            # Index 0: folder 1: filename
            dcmFiles = [[folderName, f] for f in listdir(folderName) if isfile(join(folderName, f))]
            newImages = list(filter(lambda img: f'{img[0]}/{img[1]}' not in existing_images, dcmFiles))

            UploadSwift(f"{current_directory}/{folder}", newImages)
            existing_images.update(map(lambda img: f'{img[0]}/{img[1]}', newImages))

        time.sleep(TIME_TO_WAIT_BEFORE_NEXT_UPLOAD)
