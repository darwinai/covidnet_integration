#!/bin/bash

http -a cubeadmin:cubeadmin1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=local/pl-covidnet \
 descriptor_file@jsonRepresentations/covidnet.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-covidnet

http -a cubeadmin:cubeadmin1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=fnndsc/pl-med2img \
 descriptor_file@jsonRepresentations/med2img.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-med2img

http -a cubeadmin:cubeadmin1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=pl-mri10yr06mo01da_normal \
  descriptor_file@jsonRepresentations/mri10yr06mo01da_normal.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-mri10yr06mo01da_normal