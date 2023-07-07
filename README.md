## NLP Partner Integration Application
This console app is designed to demonstrate how to integrate with the IMO NLP Api.

## Dependencies
- Python3.8

## Install the following python package
- Pandas
- Requests
- Json
```
pip install -r requirements.txt
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

- Display Entities in tabular form

Sample tabular response:

| index | semantic | text                                   | attrs.assertion | imo_lexical | icd10cm                                                                                             |
| ----- | -------- | -------------------------------------- | --------------- | ----------- | --------------------------------------------------------------------------------------------------- |
| 0     | problem  | highschool instructor                  | present         | 1526491289  | {'code': 'Y07.53', 'title': 'Teacher or instructor, perpetrator of maltreatment and neglect', 'm... |
| 1     | test     | cardiac catheterization                | present         | 689102      | NaN                                                                                                 |
| 4     | problem  | palpitations                           | present         | 27471       | {'code': 'R00.2', 'title': 'Palpitations', 'map_type': 'Preferred primary', 'code_metadata': {'c... |
| 5     | problem  | chest pressure                         | present         | 69698801    | {'code': 'R07.89', 'title': 'Other chest pain', 'map_type': 'Preferred primary', 'code_metadata'... |
| 7     | drug     | Clonidine                              | present         | 112476      | NaN                                                                                                 |
| 9     | problem  | Severe Rash  on face and leg           | present         | 41503942    | {'code': 'Z78.9', 'title': 'Other specified health status', 'map_type': 'Preferred primary', 'co... |
| 10    | problem  | slightly itchy                         | present         | 87386457    | {'code': 'Z74.09', 'title': 'Other reduced mobility', 'map_type': 'Preferred primary', 'code_met... |
| 12    | drug     | Vyvanse                                | present         | 1495475388  | NaN                                                                                                 |
| 16    | drug     | Clonidine                              | present         | 1495698898  | NaN                                                                                                 |
| 22    | problem  | Boggy inferior turbinates              | present         | 29245502    | {'code': 'C30.0', 'title': 'Malignant neoplasm of nasal cavity', 'map_type': 'Preferred primary'... |
| 25    | problem  | oropharyngeal lesion                   | absent          | 1053446     | {'code': 'J39.2', 'title': 'Other diseases of pharynx', 'map_type': 'Preferred primary', 'code_m... |
| 27    | problem  | Mild erythematous eruption to hairline | present         | 1526701     | {'code': 'L53.9', 'title': 'Erythematous condition, unspecified', 'map_type': 'Preferred primary... |

- Display Relationships in tabular form

Sample tabular response:
|     | semantic         | fromEnt.text                 | toEnt.text         |
| --- | ---------------- | ---------------------------- | ------------------ |
| 0   | test-temporal    | cardiac catheterization      | April 2019         |
| 1   | problem-temporal | chest pressure               | today              |
| 2   | problem-temporal | palpitations                 | today              |
| 3   | problem-bodyloc  | chest pressure               | chest              |
| 4   | problem-severity | Severe Rash  on face and leg | Severe             |
| 5   | problem-severity | slightly itchy               | slightly           |
| 6   | drug-frequency   | Vyvanse                      | at breakfast daily |
| 7   | drug-route       | Vyvanse                      | po                 |
| 8   | drug-strength    | Vyvanse                      | 50 mgs             |
| 9   | drug-form        | Clonidine                    | tabs               |
| 10  | drug-route       | Clonidine                    | po                 |
| 11  | drug-dosage      | Clonidine                    | 1 and 1 / 2        |
| 12  | drug-frequency   | Clonidine                    | qhs                |
| 13  | drug-strength    | Clonidine                    | 0.2 mgs            |
| 14  | problem-bodyloc  | Boggy inferior turbinates    | turbinates         |
| 15  | problem-negation | oropharyngeal lesion         | No                 |
| 16  | problem-bodyloc  | oropharyngeal lesion         | oropharyngeal      |
