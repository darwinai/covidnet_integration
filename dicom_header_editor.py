from pydicom import dcmread
from os import listdir, system
from os.path import isfile, join
import datetime

src_folder = 'src_images'
dest_folder = 'dest_images'
base_file_name = 'custom_dicom_'
data = [
    {
    'FileNameSuffix': '0',
    'PatientID': '12345678',
    'PatientName': 'Bill Ha',
    'PatientAge': '21',
    'PatientBirthDate': '2000-01-01',
    'StudyInstanceUID': '1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873080',
    'StudyDescription': 'Study Description',
    'SeriesInstanceUID': '1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873099',
    'SeriesDescription': 'Series Description',
    'StudyDate': '2021-01-01'
    }
]

src_files = [[src_folder, f] for f in listdir(src_folder) if isfile(join(src_folder, f))]
for i in range(len(data)):
    f = src_files[0]
    with open(join(f[0],f[1]), 'rb') as infile:
        ds = dcmread(infile)
        ds.PatientID = data[i].get('PatientID', '')
        ds.PatientName = data[i].get('PatientName', '')
        ds.PatientAge = data[i].get('PatientAge', '')
        ds.PatientBirthDate = data[i].get('PatientBirthDate', '')
        ds.StudyInstanceUID = data[i].get('StudyInstanceUID', '')
        ds.StudyDescription = data[i].get('StudyDescription', '')
        ds.SeriesInstanceUID = data[i].get('SeriesInstanceUID', '')
        ds.SeriesDescription = data[i].get('SeriesDescription', '')
        ds.StudyDate = data[i].get('StudyDate', '')
        file_name_suffix = data[i].get('FileNameSuffix', '')
        ds.save_as(f'{dest_folder}/{base_file_name}{file_name_suffix}.dcm')

# Print header info of DICOM files in dest_folder
dest_files = [[dest_folder, f] for f in listdir(dest_folder) if isfile(join(dest_folder, f))]
for index in range(len(dest_files)):
  f = dest_files[index]
  with open(join(f[0],f[1]), 'rb') as infile:
      ds = dcmread(infile)
      print(f[1])
      print(ds)
