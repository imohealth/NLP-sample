## NLP Partner Integration Application
This console app is designed to demonstrate how to integrate with the IMO NLP Api.

## Dependencies
- Python3.8

## Install the following python package
- Pandas
- Requests
- Json
```
pip -r requirements.txt
```

## Client Credentials
Contact IMO Client Support to get test credentials (CLIENT_ID and SECRET). Paste those values in the 'config.json'
 
## Execution
- Paste you example unstructured note on Line 6 of ./test.py as follows:
  
```
# Paste your sample  unstructured note here
unstructured_note = """Pt is 87 yo woman, highschool teacher with past medical history that includes
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
```

- Run the following command to execute

```
python .\test.py
```

## Steps to integrate
The following steps are implemented in the example test.py included in the package

- Obtain Access Token
- Read Token from Auth0 Response
- Extract token from the Auth0 response
- Prepare API Request


```
{
  "text": "A 61 year old patient has chronic pain in left leg"
}
```
- Send NLP Request

- Display Entites in tabular form

Sample tabular response:


| |  domain|                   entity| assertion.result |   related_entities | codemaps.imo.lexical_code |   codemaps.icd10cm                               |
|-| ------ | ---------------------   | ---------------- |   ---------------- | ------------------------- |   -----------------------------------------      |
|1| PROBLEM|             palpitations|      conditional |         []         |            27471          | [{'code': 'R00.2', 'title': 'Palpitations', 'm...|
|2| PROBLEM|           chest pressure|          present |         []         |         69698801          | [{'code': 'R07.89', 'title': 'Other chest pain...|
|3| PROBLEM|         Sleeping trouble|          present |         []         |           370583          | [{'code': 'G47.9', 'title': 'Sleep disorder, u...|
|4| PROBLEM|                     Rash|          present | [{'type': 'body'   |          25715457         | [{'code': 'R21', 'title': 'Rash and other nons...|
|5| PROBLEM|                    itchy|          present | [{'type': 'body'   |          41503942         | [{'code': 'Z78.9', 'title': 'Other specified'    |
|6| PROBLEM|Boggy inferior turbinates|          present |         []         |         29245502          | [{'code': 'C30.0', 'title': 'Malignant neoplas...|
|7| PROBLEM| oropharyngeal lesion    |          absent  |         []         |          1053446          | [{'code': 'J39.2', 'title': 'Other diseases of...|
|8| PROBLEM|    erythematous eruption|          present | [{'type': 'body'   |          1526701          | [{'code': 'L53.9', 'title': 'Erythematous cond...|


- Display Related Entities in tabular form

Sample tabular response:

| |      type                   |  confidence | related_entity |   domain |      entity         |assertion.result | codemaps.imo.lexical_code |codemaps.imo.confidence |
|-| --------------------------- | ----------- | -------------- | -------- | ------------------  | --------------- | ------------------------- | ---------------------- |
|0|External_body_part_or_region |    1.0      |   face and leg | PROBLEM  |       Rash          |         present |                  25715457 |                 0.707  |
|1|External_body_part_or_region | 0.99999964  |   face and leg | PROBLEM  |     itchy           |         present |                  41503942 |                 0.081  |
|2|External_body_part_or_region |       1.0   |    hairline    | PROBLEM  |erythematous eruption|         present |                  1526701  |                  0.69  |