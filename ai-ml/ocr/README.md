# Bridgesocialcare - Proof of Concept (POC) for Medication Extraction from SNF Referral Documents

To build a proof of concept (POC) for extracting scheduled and as required (PRN - Latin phrase for 'pro re nata' - 'as required') medications from skilled nursing facility (SNF) referral documents, the solution can involve the following components:

## Installation

- Clone this repo:
  ```
  git clone https://github.com/kaljuvee/ocr.git
  ```
  
- Set up a Python virtual environment and activate it (Linux):
  ```
  python3 -m venv .venv
  source .venv/bin/activate
  ```
- Install tesseract-ocr
  ```
  sudo apt install tesseract-ocr
  ```
    
- Install dependencies
  ```
  pip install -r requirements.txt
  ```
- Set .env file for the Open AI key
  ```
  copy .env.sample .env
  ```
- Replace the following line with a valid Open AI key:
  ```
  OPENAI_API_KEY = 'sk-...'
  ```   
## Running Test

- Run from command line to ensure insallation successful:
  ```
  python run extractor.py
  ```
## Running Extraction End Point as Flask

- Run Extrator Service in Flask
```
$ python extractor_service.py
 * Serving Flask app 'extractor_service'
 * Debug mode: on
2024-04-24 21:21:51,095 - 140383962300800 - _internal.py-_internal:96 - INFO: WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
2024-04-24 21:21:51,095 - 140383962300800 - _internal.py-_internal:96 - INFO: Press CTRL+C to quit
2024-04-24 21:21:51,101 - 140383962300800 - _internal.py-_internal:96 - INFO:  * Restarting with stat
2024-04-24 21:21:57,884 - 140060435247488 - _internal.py-_internal:96 - WARNING:  * Debugger is active!
2024-04-24 21:21:57,885 - 140060435247488 - _internal.py-_internal:96 - INFO:  * Debugger PIN: 652-063-290
```
## Testing Extraction Service

## Testing with CURL
- Call the service
```
curl -X POST -F "file=@/docs/sample_assessment_referral.pdf" http://localhost:5000/upload
```
- Expected output
```json
{
    "scheduled_medications": [
        {
            "name": "acetaminophen",
            "dosage": "975 mg",
            "route": "oral",
            "frequency": "Q6H",
            "location": "page 5, row 1"
        },
        {
            "name": "aspirin ec",
            "dosage": "81 mg",
            "route": "oral",
            "frequency": "daily",
            "location": "page 5, row 2"
        },
        {
            "name": "atorvastatin",
            "dosage": "80 mg",
            "route": "oral",
            "frequency": "daily",
            "location": "page 5, row 3"
        },
        {
            "name": "cyanocobalamin (vitamin B-12)",
            "dosage": "1,000 mcg",
            "route": "oral",
            "frequency": "daily",
            "location": "page 5, row 4"
        },
        {
            "name": "donepezil",
            "dosage": "5 mg",
            "route": "oral",
            "frequency": "daily",
            "location": "page 5, row 5"
        },
        {
            "name": "fluticasone propionate",
            "dosage": "1 spray",
            "route": "nasal",
            "frequency": "BID",
            "location": "page 5, row 6"
        },
        {
            "name": "Folic acid",
            "dosage": "1,000 mcg",
            "route": "oral",
            "frequency": "QAM",
            "location": "page 5, row 7"
        },
        {
            "name": "levothyroxine",
            "dosage": "37.5 mcg",
            "route": "oral",
            "frequency": "2x weekly",
            "location": "page 5, row 8"
        },
        {
            "name": "levothyroxine",
            "dosage": "75 mcg",
            "route": "oral",
            "frequency": "5x weekly",
            "location": "page 5, row 9"
        },
        {
            "name": "melatonin",
            "dosage": "5 mg",
            "route": "oral",
            "frequency": "Nightly",
            "location": "page 6, row 1"
        },
        {
            "name": "mirtazapine",
            "dosage": "15 mg",
            "route": "oral",
            "frequency": "daily",
            "location": "page 6, row 2"
        },
        {
            "name": "nicotine",
            "dosage": "21 mg/24 hr",
            "route": "transdermal",
            "frequency": "daily",
            "location": "page 6, row 3"
        },
        {
            "name": "senna",
            "dosage": "2 tablet",
            "route": "oral",
            "frequency": "Nightly",
            "location": "page 6, row 4"
        },
        {
            "name": "sennosides",
            "dosage": "17.6 mg",
            "route": "oral",
            "frequency": "Nightly",
            "location": "page 6, row 5"
        }
    ],
    "prn_medications": [
        {
            "name": "sibuterol",
            "dosage": "90 mcg/actuation",
            "route": "inhaler",
            "location": "page 6, row 1"
        },
        {
            "name": "aluminum-magnesium hydroxide-simethicone",
            "dosage": "200-200-20 mg/5 mL",
            "route": "oral",
            "location": "page 6, row 2"
        },
        {
            "name": "bisacodyl",
            "dosage": "10 mg",
            "route": "rectal",
            "location": "page 6, row 3"
        },
        {
            "name": "HYDROmorphone",
            "dosage": "0.2-0.4 mg",
            "route": "IV",
            "location": "page 6, row 4"
        },
        {
            "name": "ipratropium-albuterol",
            "dosage": "0.5-3 mg/3 mL",
            "route": "nebulizer",
            "location": "page 6, row 5"
        },
        {
            "name": "trazodone",
            "dosage": "25 mg",
            "route": "oral",
            "location": "page 6, row 6"
        }
    ]
}
```
### Testing From Browser

- click on upload_test.html in the root folder
- upload the file and press 'Submit'
- you should see the following response:

![Browser Sample JSON Response](https://github.com/kaljuvee/bridgesocialcare/blob/master/images/browser_output.png?raw=true "Browser JSON Response")

# Implementation Notes
## 1. API Design

### Upload Endpoint
- **Functionality**: Users upload the referral document (PDF) via this endpoint.
- **Process**:
  - Accept PDF upload and serve back JSON - **extactor_service.py**.
  - Extract via OCR and perform entity extraction using OpenAI - **extractor.py**

### Extraction Endpoint
- **Functionality**: Checks the status of the extraction process.
- **Returns**: Returns the medication data once available.

## 2. Medication Extraction Process

### PDF Parsing
- **Details**: Convert PDF document to a text format.
- **Focus**: Since we're dealing with standardized referrals, focus on pages 5-6 where the medications are listed.

### Text Processing
- **Techniques**: Use regular expressions or Natural Language Processing (NLP) to identify medication details.
  - **Scheduled Medications**: Include name, dosage, route, and frequency.
  - **PRN Medications**: Include name, dosage, and route.

### Data Structure
- **Format**: Organize extracted data into structured formats (e.g., JSON) to be consumed by other systems or applications.

## 3. Technology Stack

### Backend Framework
- **Service**: Flask was used to service the API endpoint.

### PDF Handling
- **Libraries**: pytesseract, pdf2image and Pillow were used for parsing PDF documents.

### NLP Tools
- **Named Entity Extraction (NER)**: OpenAI along with the optional gptcache libraries were used with very speficic prompts to perform NER.

