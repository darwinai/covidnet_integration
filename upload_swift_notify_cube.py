import swiftclient
import time
import argparse

from pydicom import dcmread
from os import listdir, system
from os.path import isfile, join

from chrisclient import client

parser = argparse.ArgumentParser(description='COVID-Net Training Script')
parser.add_argument('--mock', default=False, type=bool, help='To use Mock data or not')

args = parser.parse_args()

chris_client = client.Client("http://localhost:8000/api/v1/", "chris", "chris1234")

# Swift service settings
DEFAULT_FILE_STORAGE = 'swift.storage.SwiftStorage'
SWIFT_AUTH_URL = 'http://127.0.0.1:8080/auth/v1.0'
SWIFT_USERNAME = 'chris:chris1234'
SWIFT_KEY = 'testing'
SWIFT_CONTAINER_NAME = 'users'
folder = 'images'
output_path = 'SERVICES/PACS/covidnet'

# get all dicom images
dcmFiles = [[folder, f] for f in listdir(folder) if isfile(join(folder, f))]

for f in dcmFiles:
    system('swift -A {} -U {} '.format(SWIFT_AUTH_URL, SWIFT_USERNAME)
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


# increment the value in mock data each time
mockData = {
  'PatientID': 12345678,
  "StudyInstanceUID": 11111111,
  "SeriesInstanceUID": 22222222
}

mockBirthDate = "1994-2-10"


mockNames = [
  "Bill Ha"
]

# if the image belong here, put them in a different studyinstanceUID
differentInstance = [
  'PatientF.dcm',
  '0000.dcm',
  '0001.dcm'
]


for index in range(len(dcmFiles)):
  f = dcmFiles[index]
  with open(join(f[0],f[1]), 'rb') as infile:
      ds = dcmread(infile)
      if not args.mock:
        pacs_data = {
          'path': f'SERVICES/PACS/covidnet/{f[1]}',
          'PatientID': str(ds.PatientID), 
          'PatientName': str(ds.PatientName), 
          'PatientBirthDate': str(ds.PatientBirthDate) if ds.PatientBirthDate != '' else mockBirthDate,
          'PatientAge': str(ds.PatientAge),
          'PatientSex': str(ds.PatientSex),
          'StudyInstanceUID': str(ds.StudyInstanceUID), 
          'StudyDescription': 'Some description of the study', 
          'SeriesInstanceUID': str(ds.SeriesInstanceUID), 
          'SeriesDescription': str(ds.SeriesDescription), 
          'pacs_name': 'covidnet'
        }
      else:  # use mock
        pacs_data = {
          'path': f'SERVICES/PACS/covidnet/{f[1]}',
          'PatientID': str(mockData['PatientID']), 
          'PatientName': str(mockNames[len(mockNames)-1]) if index >= len(mockNames) else str(mockNames[index]), 
          'PatientBirthDate': str(ds.PatientBirthDate) if ds.PatientBirthDate != '' else mockBirthDate,
          'PatientAge': str(ds.PatientAge) if hasattr(ds, 'PatientAge') else 30,
          'PatientSex': str(ds.PatientSex),
          'StudyInstanceUID': str(mockData['StudyInstanceUID']) if f[1] not in differentInstance else  str(mockData['StudyInstanceUID']+2),
          'StudyDescription': 'XRay Scan for possible COVID' if f[1] not in differentInstance else "XRay Scan for possible normal", 
          'SeriesInstanceUID': str(str(mockData['SeriesInstanceUID']+index)), 
          'SeriesDescription': str(ds.SeriesDescription) if hasattr(ds, 'SeriesDescription') else 'Default Description',
          'pacs_name': 'covidnet'
        }
      try:
        chris_client.register_pacs_file(pacs_data)
      except:
        print('Already Registered: {}'.format(f[1]))
        continue
      print('SUCCESS')
