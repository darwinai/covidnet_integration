# COVID-Net Integration Repo

This repo is an integration to 
1. upload plugins to ChRIS
2. upload sample dicom image mock data. 
3. upload real hospital dicom image data from SFTP folder to swift
4. generate initial STFP folder structure for hospitals

## Installation

You can install the required python libraries by executing `./install_packages.sh` script

## Usage

1. Upload plugins to ChRIS:

   1. Run `./uploadPlugins.sh`
   
   2. Go to  `http://localhost:8000/chris-admin/plugins/plugin/add/`

   3. For each of the plugins, select `Host` as the compute resource, enter the plugin name, and Save. If there are any issues with uploading or running plugins, see the note below.

3. To monitor hospital dicom images folder and upload to swift: `python3 monitorAndUploadSwift.py`. Please check `monitorAndUploadSwift.py` for more information on the folder structure it needs to be in to work properly 
3. Run `./generateHospitalFolderStructure.sh`

**Note**: If there are any issues with uploading or running plugins, an alternative method for adding plugins is the following:

1. Go to  `http://localhost:8000/chris-admin/plugins/plugin/add/`
2. For each of the plugins, select `Host` as the compute resource, enter the corresponding URL, and Save

| Plugin                    | URL                                      |
| ------------------------- | ---------------------------------------- |
| pl-dircopy                | https://chrisstore.co/api/v1/plugins/25/ |
| pl-med2img                | https://chrisstore.co/api/v1/plugins/31/ |
| pl-covidnet               | https://chrisstore.co/api/v1/plugins/28/ |
| pl-ct-covidnet            | https://chrisstore.co/api/v1/plugins/30/ |
| pl-covidnet-pdfgeneration | https://chrisstore.co/api/v1/plugins/32/ |

## Creating more mock DICOM files

`dicom_header_editor/dicom_header_editor.py` can be used to generate new copies of existing DICOM files with modified headers (same image, but with a new Patient Name, Age, SeriesInstanceUID, etc.). It can be useful for creating new sets of DICOM files with varying header properties for manually testing COVID-Net UI. The script takes a list of objects containing the desired headers and creates a copy of an existing DICOM file for each object in that list.

When running `dicom_header_editor.py`, there are 4 arguments to pass:

* `src`: the DICOM file that will be used as reference to generate the new files.
* `dest`: the folder where the resulting files are outputted to.
* `baseName`: the desired file name prefix for the resulting files.
* `headers`: the JSON file containing an array of objects with the headers to set.

For example, `python3 dicom_header_editor.py --src=dicom.dcm --dest=dest_images --baseName=custom_ --headers=headers.json`.

An example `headers` JSON file is provided in `dicom_header_editor/headers.json`. Running the above command will generate a copy of `dicom.dcm` in `/dest_images` called `custom_0.dcm` with headers as specified in the one object listed in `headers.json`.
