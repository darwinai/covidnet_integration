#!/bin/bash

http -a chris:chris1234 -f POST http://localhost:8000/api/v1/uploadedfiles/ upload_path=chris/uploads/covidnet/ex-covid_tMQp4tR.jpeg \
 fname@<path to ex-covid_tMQp4tR.jpeg>

http -a chris:chris1234 POST http://localhost:8000/api/v1/plugins/5/instances/ \
 template:='{"data":[{"name":"dir","value":"SERVICES/PACS/covidnet/PatientA.dcm"}]}' \
 Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json

http -a chris:chris1234 POST http://localhost:8000/api/v1/plugins/5/instances/ \
 template:='{"data":[{"name":"dir","value":"SERVICES/PACS/covidnet/PatientA.dcm"}]}' \
 Content-Type:application/vnd.collection+json Accept:application/vnd.collection+json


http -a chris:chris1234 http://localhost:8000/api/v1/plugins/instances/10/