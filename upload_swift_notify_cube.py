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
    print(object_list)
    if len(object_list) < len(dcmFiles):
        time.sleep(0.2)
        poll_loop += 1


# increment the value in mock data each time
mockData = {
  'PatientID': 12345678,
  "StudyInstanceUID": 11111111,
  "SeriesInstanceUID": 22222222
}


mockNames = [
  "Bill Ha", "Example Name", "Linda Young", "Example name2", "Example name3"
]


for index in range(len(dcmFiles)):
  f = dcmFiles[index]
  with open(join(f[0],f[1]), 'rb') as infile:
      ds = dcmread(infile)
      if not args.mock:
        pacs_data = {
          'path': 'SERVICES/PACS/covidnet/{}'.format(f[1]),
          'PatientID': str(ds['0010', '0020'].value), 
          'PatientName': str(ds['0010', '0010'].value), 
          'PatientAge': str(ds['0010','1010'].value),
          'PatientSex': str(ds['0010','0040'].value),
          'StudyInstanceUID': str(ds['0020','000d'].value), 
          'StudyDescription': 'Some description of the study', 
          'SeriesInstanceUID': str(ds['0020', '000e'].value), 
          'SeriesDescription': str(ds['0008', '103e'].value), 
          'pacs_name': 'covidnet'
        }
      else:  # use mock
        pacs_data = {
          'path': 'SERVICES/PACS/covidnet/{}'.format(f[1]),
          'PatientID': str(mockData['PatientID']+index), 
          'PatientName': str(mockNames[index]) if index < len(mockNames) else str(mockNames[len(mockData)-1]), 
          'PatientAge': str(ds['0010','1010'].value),
          'PatientSex': str(ds['0010','0040'].value),
          'StudyInstanceUID': str(str(mockData['StudyInstanceUID']+index)), 
          'StudyDescription': 'Some description of the study', 
          'SeriesInstanceUID': str(str(mockData['SeriesInstanceUID']+index)), 
          'SeriesDescription': str(ds['0008', '103e'].value), 
          'pacs_name': 'covidnet'
        }
      try:
        chris_client.register_pacs_file(pacs_data)
      except:
        print('Already Registered: {}'.format(f[1]))
        continue
      print('SUCCESS')
