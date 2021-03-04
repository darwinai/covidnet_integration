# **Covidnet** Integration Repo

This repo is an integration to 
1. upload plugins to ChRIS
2. upload sample dicom image mock data. 
3. upload real hospital dicom image data from SFTP folder to swift
4. generate initial STFP folder structure for hospitals

## Installation

You can install the required python libraries by executing `./install_packages.sh` script



## Usage

1. Upload plugins to ChRIS. There are 2 options for doing this:

   1. Run `./uploadPlugins.sh`
   2. Go to  `http://localhost:8000/chris-admin/plugins/plugin/add/`
   3. For each of the plugins, select `Host` as the compute resource, enter the plugin name, and Save

   Note: It may be the case that the `pl-dircopy`, `pl-med2img`, `pl-covidnet`, or `pl-ct-covidnet` plugins fail to run due to breaking changes made to their images. If this happens, a stable version of each of the plugins can be pulled and registered instead:

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

