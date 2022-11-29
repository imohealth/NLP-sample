import json
import requests
import pandas as pd

# Paste your sample  unstructured note here
unstructured_note = """Pt is 87 yo woman, highschool instructor with past medical history that includes
   - status post cardiac catheterization in April 2019.
She presents today with palpitations and chest pressure.
HPI : Sleeping trouble on present dosage of Clonidine. Severe Rash  on face and leg, slightly itchy  
Meds : Vyvanse 50 mgs po at breakfast daily, 
            Clonidine 0.2 mgs -- 1 and 1 / 2 tabs po qhs 
HEENT : Boggy inferior turbinates, No oropharyngeal lesion 
Lungs : clear 
Heart : Regular rhythm 
Skin :  Mild erythematous eruption to hairline 

Follow-up as scheduled"""

# Obtain Access Token

print("- App started.")

with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    imo_keys = config['imo_keys']

client_id = imo_keys['CLIENT_ID']
client_secret = imo_keys['SECRET']


BASE_URL = 'https://api.imohealth.com/nlp/annotate'
audience = "https://api.imohealth.com"
grant_type = "client_credentials"
data = {
    "grant_type": grant_type,
    "client_id": client_id,
    "client_secret": client_secret,
    "audience": audience
}
auth0_auth_url = "https://auth.imohealth.com/oauth/token"
auth_response = requests.post(auth0_auth_url, data=data)

# Read token from Auth0 response
auth_response_json = auth_response.json()
auth_token = auth_response_json["access_token"]
auth_token_header_value = "Bearer %s" % auth_token


# Prepare API Request
auth_token_header = {
    'Authorization': auth_token_header_value,
    'Content-Type': 'text/plain; charset=utf-8'}

request_body = {
    "text": unstructured_note
}

# Send NLP Request
response = requests.post(BASE_URL, data= json.dumps(request_body).encode('utf-8'), headers=auth_token_header  )
json_data = json.loads(response.text)
for i in json_data['entities']:
    for j in i['related_entities']:
        j['related_entity']= j.pop('entity')

# Show Entities

dataframe = pd.json_normalize(json_data['entities'])
df = dataframe[['domain', 'entity', 'begin_offset', 'assertion.result', 'codemaps.imo.lexical_code','codemaps.imo.confidence',  'codemaps.icd10cm']]
print('=================================================')
print('Entities extracted')
print('=================================================')
print(df)
print('=================================================')
print('Entity Relationships to body part and laterality')
print('=================================================')
df = pd.json_normalize(json_data['entities'], record_path=['related_entities'], meta=['domain', 'entity', ['assertion', 'result'], ['codemaps', 'imo', 'lexical_code'], ['codemaps', 'imo', 'confidence']])
print(df)
