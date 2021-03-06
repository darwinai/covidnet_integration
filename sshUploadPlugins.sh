#!/bin/bash

http -a chris:chris1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=local/pl-covidnet \
 descriptor_file@jsonRepresentations/covidnet.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-covidnet

http -a chris:chris1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=fnndsc/pl-med2img \
 descriptor_file@jsonRepresentations/med2img.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-med2img

http -a chris:chris1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=local/pl-ct-covidnet \
 descriptor_file@jsonRepresentations/ct_covidnet.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-ct-covidnet

http -a chris:chris1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=fnndsc/pl-dircopy \
 descriptor_file@jsonRepresentations/dircopy.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-dircopy

http -a chris:chris1234 -f POST http://localhost:8010/api/v1/plugins/ dock_image=local/pl-pdfgeneration \
 descriptor_file@jsonRepresentations/pdfgeneration.json public_repo=https://github.com/FNNDSC/pl-simplefsapp name=pl-pdfgeneration
