# COVID-Net Integration Repo

This repo is an integration to 
1. upload plugins to ChRIS
2. upload sample dicom image mock data. 
3. upload real hospital dicom image data from SFTP folder to swift
4. generate initial STFP folder structure for hospitals

## Installation

You can install the required python libraries by running `./install_packages.sh`

Install httpie through the following instructions: https://httpie.io/docs#installation

## Usage

### If building from source:

1. Upload plugins to ChRIS:

   1. Run `./uploadPlugins.sh`
   
   2. Go to  `http://localhost:8000/chris-admin/plugins/plugin/add/`

   3. For each of the plugins, select `Host` as the compute resource, enter the plugin name, and Save. If there are any issues with uploading or running plugins, see the note below.

2. Run `./generateHospitalFolderStructure.sh`

3. To monitor hospital dicom images folder and upload to swift: `python3 monitorAndUploadSwift.py`. Please check `monitorAndUploadSwift.py` for more information on the folder structure it needs to be in to work properly 

### If pulling from dockerhub (using latest stable versions):

1. Copy `postscript.sh` into `ChRIS_ultron_backEnd`, replacing the default one that exists in that folder
2. After the CUBE backend has been instantiated using `make.sh`, run `./postscript.sh`

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

## Uploading DICOM files to Swift

There are a few DICOMs sample with generated fake-metadata:

|           | Fake MRN  | Image Name                                                          | Prediction Confidences (With COVID-Net CXR4 A) |        |       | Study Date | Patient Name      | Birthdate  | Age | Sex | AE Title | Modality | Study Instance UID                                     | Study Description                  | Series Instance UID                                    | Series Description / Protocol Name |
| --------- | --------- | ------------------------------------------------------------------- | ---------------------------------------------- | ------ | ----- | ---------- | ----------------- | ---------- | --- | --- | -------- | -------- | ------------------------------------------------------ | ---------------------------------- | ------------------------------------------------------ | ---------------------------------- |
| COVID-19  | DAI000068 | 16654\_1\_1.png                                                     | 0.804                                          | 0.024  | 0.172 | 2020-12-06 | Michael Garcia    | 1951-03-24 | 70  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873077 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873082 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000196 | COVID-19(70).png                                                    | 0.999                                          | 0.001  | 0     | 2021-03-06 | Brian Moore       | 1963-01-09 | 58  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873060 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873032 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000247 | covid-19-pneumonia-mild.JPG                                         | 0.941                                          | 0.004  | 0.055 | 2020-05-19 | Nancy Davis       | 1962-12-27 | 58  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873075 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873084 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000322 | B2D20576-00B7-4519-A415-72DE29C90C34.jpeg                           | 0.991                                          | 0.009  | 0     | 2020-07-07 | William Ha        | 1975-11-18 | 45  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873080 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873099 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000469 | 16654\_2\_1.jpg                                                     | 0.757                                          | 0.23   | 0.013 | 2020-04-27 | Laura Collins     | 1998-02-19 | 23  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873076 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873083 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000495 | CR.1.2.840.113564.1722810170.20200325212815187370.1003000225002.png | 1                                              | 0      | 0     | 2020-06-30 | Jennifer Perez    | 1987-12-07 | 33  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873078 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873081 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000531 | 1-s2.0-S0929664620300449-gr2\_lrg-a.jpg                             | 1                                              | 0      | 0     | 2020-11-26 | Mary Brown        | 1957-01-21 | 64  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873070 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873089 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000652 | 1B734A89-A1BF-49A8-A1D3-66FAFA4FAC5D.jpeg                           | 0.998                                          | 0      | 0.02  | 2020-08-28 | Robert Johnson    | 1947-06-20 | 73  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873074 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873085 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000787 | DX.1.2.840.113564.1722810162.20200415105839964650.1203801020003.png | 1                                              | 0      | 0     | 2020-09-16 | Daniel Jones      | 1983-08-31 | 37  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873079 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873031 | XR Posteroanterior (PA) view       |
| COVID-19  | DAI000943 | 9C34AF49-E589-44D5-92D3-168B3B04E4A6.jpeg                           | 0.78                                           | 0.189  | 0.031 | 2021-01-15 | Jacob Miller      | 1936-04-05 | 85  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873073 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873086 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000036 | 2c68016e-5a63-4430-a834-efe5d43edd0e.png                            | 0                                              | 0.999  | 0.001 | 2020-10-17 | Benjamin Wilson   | 1968-02-27 | 53  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873072 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873087 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000095 | baf8fe18-a7ca-4e9c-b3dc-5c80d474545b.png                            | 0                                              | 1      | 0     | 2020-08-30 | Emily Hernandez   | 1991-10-30 | 29  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873061 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873033 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000157 | 6565a9e6-3f01-4de8-a18d-ade3121c5d7c.png                            | 0                                              | 1      | 0     | 2020-12-29 | Richard Baker     | 1989-07-09 | 31  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873067 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873039 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000366 | 6df82c7a-a91e-487c-ae3a-9022b17d7c7a.png                            | 0.019                                          | 0.971  | 0.01  | 2020-07-14 | Alice Carter      | 1954-01-22 | 67  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873065 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873037 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000627 | 3f2b878e-9e3b-410b-a739-b43d81b98692.png                            | 0                                              | 0.999  | 0.001 | 2021-02-24 | Victoria Mitchell | 2001-03-18 | 20  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873064 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873036 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000730 | streptococcus-pneumoniae-pneumonia-temporal-evolution-1-day0.jpg    | 0.007                                          | 0.993  | 0     | 2020-05-19 | Jonathan Lee      | 1989-02-27 | 32  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873063 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873035 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000813 | 070c921f-171c-420c-915b-e49e3f600c38.png                            | 0.005                                          | 0.994  | 0     | 2020-04-08 | Elizabeth Harris  | 1977-04-01 | 44  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873068 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873021 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000828 | 1c0a780d-1cac-4eee-b46d-470ecebc9ae0.png                            | 0                                              | 0.977  | 0.023 | 2020-12-12 | Patrick Hill      | 1937-12-14 | 83  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873062 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873034 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000859 | 4bc8ce99-2420-48c2-a768-d067da67ced2.png                            | 0                                              | 1      | 0     | 2021-03-02 | Sarah Wong        | 1994-09-13 | 26  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873066 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873038 | XR Posteroanterior (PA) view       |
| Pneumonia | DAI000927 | e1d5a233-39ca-41dc-a289-b07c3e78cdb1.png                            | 0                                              | 0.999  | 0.001 | 2020-02-19 | Olivia Martinez   | 1999-07-03 | 21  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873081 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873098 | XR Posteroanterior (PA) view       |
| Normal    | DAI000118 | 4b1cab8a-c9bd-40e6-bc86-23c6be98a099.png                            | 0                                              | 0.025  | 0.975 | 2020-11-13 | Thomas Parker     | 1979-03-16 | 42  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873056 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873028 | XR Posteroanterior (PA) view       |
| Normal    | DAI000264 | a0b9597d-93f4-4a7c-a412-81cb78bccb66.png                            | 0                                              | 0.0389 | 0.961 | 2020-06-11 | Carol Thompson    | 1958-11-05 | 62  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873053 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873025 | XR Posteroanterior (PA) view       |
| Normal    | DAI000290 | f3b015ab-e337-4e7f-971d-eb7cc3dd4e92.png                            | 0                                              | 0.006  | 0.994 | 2020-09-22 | George Smith      | 1950-03-07 | 71  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873082 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873097 | XR Posteroanterior (PA) view       |
| Normal    | DAI000398 | 3e1b619a-cdd9-495a-bcbf-a9d62b418991.png                            | 0                                              | 0.026  | 0.974 | 2020-08-04 | Linda Taylor      | 1966-03-28 | 55  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873054 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873026 | XR Posteroanterior (PA) view       |
| Normal    | DAI000421 | 47c78742-4998-4878-aec4-37b11b1354ac.png                            | 0                                              | 0.001  | 0.999 | 2020-03-26 | Susan Hall        | 1941-06-24 | 79  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873050 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873022 | XR Posteroanterior (PA) view       |
| Normal    | DAI000523 | e1d23cbe-213d-48d6-a8c2-672c4e68285d.png                            | 0                                              | 0.088  | 0.912 | 2020-05-09 | Kevin Nguyen      | 1997-04-01 | 24  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873051 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873023 | XR Posteroanterior (PA) view       |
| Normal    | DAI000546 | c2b24ebd-2c40-48c3-ba39-177224dd7db0.png                            | 0                                              | 0.009  | 0.991 | 2020-03-08 | Ella Sanchez      | 2000-08-30 | 20  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873057 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873029 | XR Posteroanterior (PA) view       |
| Normal    | DAI000672 | ffba6230-71cf-4287-a0d1-887f5d16e95d.png                            | 0                                              | 0.015  | 0.985 | 2020-04-17 | Jessica Song      | 1992-09-14 | 28  | F   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873071 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873088 | XR Posteroanterior (PA) view       |
| Normal    | DAI000733 | 3a5327d8-8830-4ae2-bd6b-293f5aa42d4b.png                            | 0                                              | 0.014  | 0.986 | 2021-02-27 | Richard Nelson    | 1975-07-22 | 45  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873052 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873024 | XR Posteroanterior (PA) view       |
| Normal    | DAI000982 | 89dd8f63-8320-48f3-b142-d903f40d5c8c.png                            | 0                                              | 0.031  | 0.969 | 2021-01-29 | Alexander King    | 1985-02-21 | 36  | M   |          |          | 1.2.276.0.7230010.3.1.2.8323329.8519.1517874337.873055 | Chest X-ray for COVID-19 Screening | 1.2.276.0.7230010.3.1.3.8323329.8519.1517874337.873027 | XR Posteroanterior (PA) view       |

To import the above samples, execute the following commands:

```shell
cd <path to the covidnet_integration repo>
./make.sh
docker run --network host -v "$PWD/images/WithProtocolName/COVID-19:/images" covidnet_integration upload_swift_notify_cube.py --imageDir /images
docker run --network host -v "$PWD/images/WithProtocolName/Normal:/images" covidnet_integration upload_swift_notify_cube.py --imageDir /images
docker run --network host -v "$PWD/images/WithProtocolName/Pneumonia:/images" covidnet_integration upload_swift_notify_cube.py --imageDir /images
```

## Creating more mock DICOM files

`dicom_header_editor/dicom_header_editor.py` can be used to generate new copies of existing DICOM files with modified headers (same image, but with a new Patient Name, Age, SeriesInstanceUID, etc.). It can be useful for creating new sets of DICOM files with varying header properties for manually testing COVID-Net UI. The script takes a list of objects containing the desired headers and creates a copy of an existing DICOM file for each object in that list.

When running `dicom_header_editor.py`, there are 4 arguments to pass:

* `src`: the DICOM file that will be used as reference to generate the new files.
* `dest`: the folder where the resulting files are outputted to.
* `baseName`: the desired file name prefix for the resulting files.
* `headers`: the JSON file containing an array of objects with the headers to set.

For example, `python3 dicom_header_editor.py --src=dicom.dcm --dest=dest_images --baseName=custom_ --headers=headers.json`.

An example `headers` JSON file is provided in `dicom_header_editor/headers.json`. Running the above command will generate a copy of `dicom.dcm` in `/dest_images` called `custom_0.dcm` with headers as specified in the one object listed in `headers.json`.
