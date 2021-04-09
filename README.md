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
   3. For each of the plugins, select `Host` as the compute resource, enter the plugin name, and Save

   

   Note: It may be the case that the `pl-dircopy`, `pl-med2img`, `pl-covidnet`, or `pl-ct-covidnet` plugins fail to run due to breaking changes made to their images. If this happens, a stable version of each of the plugins can be pulled and registered instead :

   1. Pull the Docker images:

   ```
   docker pull fnndsc/pl-dircopy:2.1.0
   docker pull fnndsc/pl-med2img:1.1.0.1
   docker pull fnndsc/pl-covidnet:0.2.0
   docker pull fnndsc/pl-ct-covidnet:0.2.0
   ```

   2. Register the plugins via CLI or UI:

      **Via CLI**

      `cd` into the `ChRIS_ultron_backEnd` repo and run the commands to register the plugins:

      | Plugin         | Command                                                      |
      | -------------- | ------------------------------------------------------------ |
      | pl-dircopy     | `docker-compose -f docker-compose_dev.yml exec chris_dev python plugins/services/manager.py register --pluginurl https://chrisstore.co/api/v1/plugins/25/ host` |
      | pl-med2img     | `docker-compose -f docker-compose_dev.yml exec chris_dev python plugins/services/manager.py register --pluginurl https://chrisstore.co/api/v1/plugins/31/ host` |
      | pl-covidnet    | `docker-compose -f docker-compose_dev.yml exec chris_dev python plugins/services/manager.py register --pluginurl https://chrisstore.co/api/v1/plugins/30/ host` |
      | pl-ct-covidnet | `docker-compose -f docker-compose_dev.yml exec chris_dev python plugins/services/manager.py register --pluginurl https://chrisstore.co/api/v1/plugins/28/ host` |

      **Via UI**	

      1. Go to  `http://localhost:8000/chris-admin/plugins/plugin/add/`
      2. For each of the plugins, select `Host` as the compute resource, then add the corresponding URL, and Save

      | Plugin         | URL                                      |
      | -------------- | ---------------------------------------- |
      | pl-dircopy     | https://chrisstore.co/api/v1/plugins/25/ |
      | pl-med2img     | https://chrisstore.co/api/v1/plugins/31/ |
      | pl-covidnet    | https://chrisstore.co/api/v1/plugins/30/ |
      | pl-ct-covidnet | https://chrisstore.co/api/v1/plugins/28/ |

2. To upload mock dicom images: `./run_mock.sh`

3. To monitor hospital dicom images folder and upload to swift: `python3 monitorAndUploadSwift.py`

Please check monitorAndUploadSwift.py for more information on the folder structure it needs to be in to work properly 

4. run `./generateHospitalFolderStructure.sh`

## Creating more mock DICOM files

`dicom_header_editor/dicom_header_editor.py` can be used to generate new copies of existing DICOM files with modified headers (same image, but with a new Patient Name, Age, SeriesInstanceUID, etc.). It can be useful for creating new sets of DICOM files with varying header properties for manually testing COVID-Net UI. The script takes a list of objects containing the desired headers and creates a copy of an existing DICOM file for each object in that list.

When running `dicom_header_editor.py`, there are 4 arguments to pass:

* `src`: the DICOM file that will be used as reference to generate the new files.
* `dest`: the folder where the resulting files are outputted to.
* `baseName`: the desired file name prefix for the resulting files.
* `headers`: the JSON file containing an array of objects with the headers to set.

For example, `python3 dicom_header_editor.py --src=dicom.dcm --dest=dest_images --baseName=custom_ --headers=headers.json`.

An example `headers` JSON file is provided in `dicom_header_editor/headers.json`. Running the above command will generate a copy of `dicom.dcm` in `/dest_images` called `custom_0.dcm` with headers as specified in the one object listed in `headers.json`.
