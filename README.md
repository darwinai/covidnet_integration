# COVID-Net Integration Repo

This repo is an integration to 
1. upload plugins to ChRIS
2. upload sample dicom image mock data. 
3. upload real hospital dicom image data from SFTP folder to swift
4. generate initial STFP folder structure for hospitals

## Installation

You can install the required python libraries by executing `./install_packages.sh` script

## Usage

1. To upload plugins to ChRIS: `./sshUploadPlugins.sh`

2. To upload mock dicom images: `./run_mock.sh`

3. To monitor hospital dicom images folder and upload to swift: `python3 monitorAndUploadSwift.py`

Please check monitorAndUploadSwift.py for more information on the folder structure it needs to be in to work properly 

4. run `./generateHospitalFolderStructure.sh`

## Creating more mock DICOM files

`dicom_header_editor.py` can be used to generate new copies of existing DICOM files with modified headers (same image, but with a new Patient Name, Age, SeriesInstanceUID, etc.). It can be useful for creating new sets of DICOM files with varying header properties for manually testing COVID-Net UI.

At the top of `dicom_header_editor.py` are 4 variables to set:

* `src_folder`: the folder that will contain the DICOM file to create copies from.
* `dest_folder`: the folder where the resulting copies are outputted to.
* `base_file_name`: the desired file name prefix for the resulting copies.
* `data`: an array of objects, each containing the most relevant DICOM header properties and their desired values. The script will output as many copies as there are objects in this array.

The script can be run using `python3 dicom_header_editor.py`.