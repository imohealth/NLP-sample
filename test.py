import json
import requests
import pandas as pd

from models import NLPResult

import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='NLP Sample Script')
parser.add_argument('--output', choices=['table', 'json', 'fhir'], default='table', help='Output format')
args = parser.parse_args()

# Set output format
output_format = args.output

# Paste your sample unstructured note here
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

# Select a pipeline to use for entity extraction
# See GET https://api.imohealth.com/entityextraction/pipelines for all available pipelines
pipeline = 'imo-clinical-comprehensive'

print("- App started.")

# 1. Obtain Access Token
with open('config.json', 'r') as config_file:
    config = json.load(config_file)
    imo_keys = config['imo_keys']

client_id = imo_keys['CLIENT_ID']
client_secret = imo_keys['SECRET']

BASE_URL = f'https://api.imohealth.com/entityextraction/pipelines/{pipeline}'
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

# 2. Read token from Auth0 response
auth_response_json = auth_response.json()
if auth_response.status_code != 200:
    raise Exception(auth_response_json["error_description"] if "error_description" in auth_response_json else "Authentication Error!")

auth_token = auth_response_json["access_token"]
auth_token_header_value = "Bearer %s" % auth_token

# 3. Send NLP API Request
headers = {
    'Authorization': auth_token_header_value,
    'Content-Type': 'application/json',
    'Accept': 'application/json' if output_format != 'fhir' else 'application/fhir+json'
}

request_body ={
    "text": unstructured_note,
    "preferences": {
        "thresholds": {
            "global": 0.0
        },
        "type_filter": ["entities", "relations"]
    }
}

response = requests.post(BASE_URL, data=  json.dumps(request_body).encode('utf-8'), headers=headers)
response.raise_for_status()

# 4. Parse and print NLP API Response
if output_format == 'json' or output_format == 'fhir':
    print('=================================================')
    print(f'NLP API {output_format} Response')
    print('=================================================')
    # Print the JSON text with pretty formatting
    print(json.dumps(json.loads(response.text), indent=4))
else: 
    result = NLPResult(**json.loads(response.text))

    pd.options.display.max_colwidth = 100

    #4. Display Entities in tabular form
    if len(result.entities) > 0:
        df = pd.json_normalize(result.entities)
        df = df[["semantic", "text", "assertion", "codemaps.imo.default_lexical_code", "codemaps.icd10cm.codes"]]
        df = df.rename(columns={'codemaps.icd10cm.codes': 'icd10cm', 'codemaps.imo.default_lexical_code': 'imo_lexical'})
        df = df[df["imo_lexical"].notna()]
        df = df.explode("icd10cm")
        print('=================================================')
        print('Entities extracted')
        print('=================================================')
        print(df)
    else:
        print("No Entities Found")

    #5. Display Relationships in tabular form
    if len(result.relations) > 0:
        df = pd.json_normalize(result.relations)
        df = df[["semantic", "from_ent_text", "to_ent_text"]]
        print('=================================================')
        print('Relations extracted')
        print('=================================================')
        print(df)
    else:
        print("No Relations Found")