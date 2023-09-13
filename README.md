## NLP Partner Integration Application
This console app is designed to demonstrate how to integrate with the IMO Precision Normalize NLP API.

## Dependencies
- Python3.8

## Install the following python package
- Pandas
- Requests
- Json
  
```sh
pip install -r requirements.txt
```

## Client Credentials
Contact IMO Client Support to get test credentials (CLIENT_ID and SECRET). Paste those values in the 'config.json'
 
## Execution
1. Paste your example unstructured note on Line 8 of [test.py](./test.py) as follows:
    ```python
    # Paste your sample unstructured note here
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
2. Set the pipeline name you want to us on Line 23 of [test.py](./test.py). You can execute a GET request to https://api.imohealth.com/entityextraction/pipelines using your API credentials to view all available pipelines, or see the [documentation](https://developer.imohealth.com/api-catalog/entity-extraction/pipelines). 
   ```python
   pipeline = 'imo-clinical-comprehensive'
   ```
3. Run the following command to execute

```sh
python .\test.py
```

## Steps to integrate
The following steps are implemented in the example [test.py](./test.py) included in the package

1. Obtain Access Token
2. Read Token from Auth0 Response
3. Send NLP API Request
4. Display Entities in tabular form (sample below)

    |     | semantic | text                                   | assertion | imo_lexical | icd10cm                                                                                             |
    | --- | -------- | -------------------------------------- | --------- | ----------- | --------------------------------------------------------------------------------------------------- |
    | 0   | test     | cardiac catheterization                | present   | 30984733    | NaN                                                                                                 |
    | 1   | problem  | palpitations                           | present   | 27471       | {'code': 'R00.2', 'title': 'Palpitations', 'map_type': 'Preferred primary', 'code_metadata': {'c... |
    | 2   | problem  | chest pressure                         | present   | 69698801    | {'code': 'R07.89', 'title': 'Other chest pain', 'map_type': 'Preferred primary', 'code_metadata'... |
    | 3   | problem  | Sleeping trouble                       | present   | 370583      | {'code': 'G47.9', 'title': 'Sleep disorder, unspecified', 'map_type': 'Preferred primary', 'code... |
    | 4   | drug     | Clonidine                              | present   | 112476      | NaN                                                                                                 |
    | 5   | problem  | Severe Rash                            | present   | 1493345662  | {'code': 'R21', 'title': 'Rash and other nonspecific skin eruption', 'map_type': 'Preferred prim... |
    | 6   | problem  | itchy                                  | present   | 52810       | {'code': 'L29.9', 'title': 'Pruritus, unspecified', 'map_type': 'Preferred primary', 'code_metad... |
    | 7   | drug     | Vyvanse                                | present   | 250630      | NaN                                                                                                 |
    | 8   | drug     | Clonidine                              | present   | 112476      | NaN                                                                                                 |
    | 9   | problem  | Boggy inferior turbinates              | present   | 29245502    | {'code': 'C30.0', 'title': 'Malignant neoplasm of nasal cavity', 'map_type': 'Preferred primary'... |
    | 10  | problem  | oropharyngeal lesion                   | absent    | 1053446     | {'code': 'J39.2', 'title': 'Other diseases of pharynx', 'map_type': 'Preferred primary', 'code_m... |
    | 11  | problem  | Mild erythematous eruption to hairline | present   | 1526701     | {'code': 'L53.9', 'title': 'Erythematous condition, unspecified', 'map_type': 'Preferred primary... |

5. Display Relationships in tabular form (sample below)
    | id  | semantic         | from_ent_text             | to_ent_text        |
    | --- | ---------------- | ------------------------- | ------------------ |
    | 0   | test-temporal    | cardiac catheterization   | April 2019         |
    | 1   | problem-temporal | chest pressure            | today              |
    | 2   | problem-temporal | palpitations              | today              |
    | 3   | problem-bodyloc  | chest pressure            | chest              |
    | 4   | problem-bodyloc  | Severe Rash               | leg                |
    | 5   | problem-bodyloc  | Severe Rash               | face               |
    | 6   | problem-severity | Severe Rash               | Severe             |
    | 7   | problem-severity | itchy                     | slightly           |
    | 8   | drug-frequency   | Vyvanse                   | at breakfast daily |
    | 9   | drug-route       | Vyvanse                   | po                 |
    | 10  | drug-strength    | Vyvanse                   | 50 mgs             |
    | 11  | drug-form        | Clonidine                 | tabs               |
    | 12  | drug-route       | Clonidine                 | po                 |
    | 13  | drug-dosage      | Clonidine                 | 1 and 1 / 2        |
    | 14  | drug-frequency   | Clonidine                 | qhs                |
    | 15  | drug-strength    | Clonidine                 | 0.2 mgs            |
    | 16  | problem-bodyloc  | Boggy inferior turbinates | turbinates         |
    | 17  | problem-negation | oropharyngeal lesion      | No                 |
    | 18  | problem-bodyloc  | oropharyngeal lesion      | oropharyngeal      |
