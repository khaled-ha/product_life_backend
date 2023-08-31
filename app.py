import json
import base64
from typing import List, Dict, Annotated, Optional, Union
import requests
from requests.auth import HTTPBasicAuth
from fastapi import FastAPI, File, UploadFile, Body, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

allowed_origins = ['http://localhost:3000', 'http://0.0.0.0:3000']
allowed_methods = ['POST, GET']

class ContactUs(BaseModel):
    firstName: str
    lastName: str
    email: str
    phone: str
    company: str
    country: str
    subject: str
    lineOfBusiness: str
    message: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=['*'],
    allow_headers=['*'],
)

def map_country_code(country)-> str:
    countries = {
        'canada':'CN',
        'united_state': 'US'
    }
    if country in countries.keys():
        return countries[country]
    return 'US'

@app.post('/contact_us')
async def contact_us(
    firstName: str,
    lastName: str,
    email: str,
    phone: str,
    company: str,
    country: str,
    subject: str,
    lineOfBusiness: str,
    message: str,
    # contact_us: ContactUs = Body(...),
    file: UploadFile = File(...),
    ):
    url = 'https://my356981.crm.ondemand.com/sap/c4c/odata/v1/c4codataapi/LeadCollection'
    # import ipdb;ipdb.set_trace()
    file_content = await file.read()
    base_64_file = base64.b64encode(file_content)
    data = {
      'Name': firstName + ' '+ lastName,
      'NameLanguageCode': 'FR',
      'QualificationLevelCode': '03',
      'UserStatusCode': '02',
      'OriginTypeCode': '002',
      'PriorityCode': '3',
      'DivisionCode': '01',
      'Company': company,
      'Note': 'Ici un affichage complet de mes notes en passant simplement la souris dessus.',
      'AccountPostalAddressElementsHouseID': '66',
      'AccountPostalAddressElementsStreetPrefix': '',
      'AccountPostalAddressElementsAdditionalStreetPrefixName': '',
      'AccountPostalAddressElementsStreetName': 'Hudson Boulevard East New York',
      'AccountPostalAddressElementsStreetSufix': '',
      'AccountPostalAddressElementsAdditionalStreetSuffixName': '',
      'AccountCity': 'New-York',
      'AccountCountry': map_country_code(country),
      'AccountState': 'NY',
      'AccountPostalAddressElementsPOBoxID': '',
      'AccountPostalAddressElementsStreetPostalCode': '10001-2192',
      'AccountPostalAddressElementsCountyName': '',
      'AccountPhone': phone,
      'AccountFax': '',
      'AccountMobile': '',
      'AccountEMail': email,
      'AccountWebsite': 'https://www.pfizer.com',
      'AccountLatitudeMeasure': '0.00000000000000',
      'AccountLatitudeMeasureUnitCode': '',
      'AccountLongitudeMeasure': '0.00000000000000',
      'AccountLongitudeMeasureUnitCode': '',
      'AccountLegalForm': '',
      'OrganisationAccountABCClassificationCode': 'B',
      'OrganisationAccountIndustrialSectorCode': '',
      'AccountCorrespondenceLanguageCode': 'EN',
      'AccountNote': '',
      'BusinessPartnerRelationshipContactVIPReasonCode': '',
      'ContactAllowedCode': '3',
      'BusinessPartnerRelationshipEngagementScoreNumberValue': '0 ',
      'ContactBuildingID': '',
      'ContactEMailUsageDeniedIndicator': '',
      'ContactNote': message,
    #   'LeadAttachmentFolder': json.dumps({
    #         'Binary': base_64_file.hex(),
    #         'CategoryCode': '2',
    #         'MimeType': 'text/plain',
    #         'Name': file.filename,
    #         'TypeCode': '10001',
    #         })
}
    # 'LeadAttachmentFolder': {
            # 'Binary': str(file_content),
            # 'CategoryCode': '2',
            # 'MimeType': 'text/plain',
            # 'Name': file.filename,
            # 'TypeCode': '10001',
            # }
    header = {'content-type': 'application/json', 'Accept': '*/*'}
    resp = requests.post(
        url,
        auth=('_FSM_0', 'Notionedge@2023'),
        json=data,
        headers=header
        )
    # import ipdb;ipdb.set_trace()
    return { 'res': 'success' }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)