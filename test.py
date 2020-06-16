import json


def makeTemplate(descriptors_dict):
    """
    Static method to make a Collection+Json template from a regular dictionary whose
    properties are the item descriptors.
    """
    template = {'data': []}
    for key in descriptors_dict:
        template['data'].append({'name': key, 'value': descriptors_dict[key]})
    return {'template': template}


res = json.dumps(makeTemplate({
  'path': 'SERVICES/PACS/covidnet/PatientB.dcm', 
  'PatientID': '0a0f6755-610d-4b7c-a460-5f5a8f5c0743', 
  'PatientName': '0a0f6755-610d-4b7c-a460-5f5a8f5c0743', 
  'PatientAge': '63', 
  'PatientSex': 'M', 
  'StudyInstanceUID': '1.2.276.0.7230010.3.1.2.8323329.15461.1517874385.807051', 
  'StudyDescription': 'Some description of the study', 
  'SeriesInstanceUID': '1.2.276.0.7230010.3.1.3.8323329.15461.1517874385.807050', 
  'SeriesDescription': 'view: PA', 
  'pacs_name': 'covidnet'
}))

print(res)