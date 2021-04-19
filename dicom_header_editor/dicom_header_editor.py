from pydicom import dcmread
from os import listdir, system
from os.path import isfile, join
import json
import datetime
import argparse

parser = argparse.ArgumentParser(description='DICOM header editor script')
parser.add_argument('--src', default="src.dcm", type=str, help='Reference DICOM file')
parser.add_argument('--dest', default="dest", type=str, help='Folder to output new DICOM files')
parser.add_argument('--baseName', default="custom_", type=str, help='Output DICOM file prefix')
parser.add_argument('--headers', default="headers.json", type=str, help='JSON containing array of objects with desired DICOM headers')

args = parser.parse_args()

src = args.src
dest_folder = args.dest
base_file_name = args.baseName

with open(args.headers, 'rb') as data:
    headers = json.load(data)
    for i in range(len(headers)):
        with open(src, 'rb') as infile:
            ds = dcmread(infile)
            ds.PatientID = headers[i].get('PatientID', '')
            ds.PatientName = headers[i].get('PatientName', '')
            ds.PatientAge = headers[i].get('PatientAge', '')
            ds.PatientBirthDate = headers[i].get('PatientBirthDate', '')
            ds.StudyInstanceUID = headers[i].get('StudyInstanceUID', '')
            ds.StudyDescription = headers[i].get('StudyDescription', '')
            ds.SeriesInstanceUID = headers[i].get('SeriesInstanceUID', '')
            ds.SeriesDescription = headers[i].get('SeriesDescription', '')
            ds.StudyDate = headers[i].get('StudyDate', '')
            ds.ProtocolName = headers[i].get('ProtocolName', '')
            file_name_suffix = headers[i].get('FileNameSuffix', '')
            ds.save_as(f'{dest_folder}/{base_file_name}{file_name_suffix}.dcm')

# Print header info of DICOM files in dest_folder
dest_files = [[dest_folder, f] for f in listdir(dest_folder) if isfile(join(dest_folder, f))]
for index in range(len(dest_files)):
  f = dest_files[index]
  with open(join(f[0],f[1]), 'rb') as infile:
      ds = dcmread(infile)
      print(f[1])
      print(ds, '\n')
