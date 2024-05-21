import json
import logging
import time
import pandas as pd
import pytesseract
from pdf2image import convert_from_path
import openai
from openai import OpenAI
from dotenv import load_dotenv
import os
from gptcache import cache  # Assuming this is a custom module for cache management
from io import StringIO
# Setup logging
# Set up basic configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='app.log',  # Specify the file where logs are written
    filemode='w'  # 'w' for overwrite each time the app starts, 'a' for append
)

# Load the environment variables from the .env file
load_dotenv()

client = OpenAI()
cache.init()
cache.set_openai_key()  # Make sure this function actually sets the API key for the client

PDF_PATH = 'docs/sample_assessment_referral.pdf'
BEGIN_PAGE = 5
END_PAGE = 6
PRN_OUT_FILE = 'prn_output.csv'
SCH_OUT_FILE = 'sch_output.csv'

def convert_to_df(data):
    """Converts CSV string to a pandas DataFrame."""
    try:
        # Create a DataFrame from the CSV data
        df = pd.read_table(StringIO(data))
        df.dropna(how="all", axis=1, inplace=True)  # Remove columns that are entirely NaN
        df.dropna(how="all", axis=0, inplace=True)  # Remove rows that are entirely NaN
        df.columns = df.columns.str.strip()  # Strip whitespace from headers
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Strip cell values
        return df
    except Exception as e:
        raise Exception(f"Failed to convert CSV to DataFrame: {e}")

def convert_images(pdf_path=PDF_PATH, first_page=BEGIN_PAGE, last_page=END_PAGE):
    """Convert specified pages of the PDF to images."""
    try:
        images = convert_from_path(pdf_path, first_page=first_page, last_page=last_page, dpi=300)
        return images
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF pages to images: {e}")

def extract_text(images):
    """Extract text using OCR from the given images, including page numbers."""
    texts = []
    page_number = BEGIN_PAGE  # Initialize page number based on the first page processed
    try:
        for image in images:
            text = pytesseract.image_to_string(image)
            # Append page number to each page's text
            page_text = f"Page {page_number}: {text}"
            texts.append(page_text)
            page_number += 1  # Increment the page number for each image
        return " ".join(texts)  # Combine texts from all images into one string
    except Exception as e:
        raise RuntimeError(f"OCR processing failed: {e}")

def extract_entities(text):
    """Use the OpenAI API to extract structured data from the text."""
    prompt = f"""
    Directly extract the medication data from the following text into two separate tables without adding any comments or explanations, or markups such as ```json or ```, only pure JSON. 

    Text section:
    {text}

    First table in the input document is 'Scheduled' with columns: Medication (Name), Ordered Dose/Rate, Route, Frequency.
    Second table input document is 'PRN' with columns: Medication (Name), Ordered Dose/Rate, Route.
    Ensure that the output strictly adheres to JSON format provided below.
    Pay attentoin to and include the page number of the text where the data was found and the row number in the table where the data was found.

    Example Format:
    {{
    "scheduled_medications": [
    {{
    "name": "Atorvastatin",
    "dosage": "20 mg",
    "route": "oral",
    "frequency": "once daily",
    "location": "page 5, row 2"
    }}
    ],
    "prn_medications": [
    {{
    "name": "Ibuprofen",
    "dosage": "400 mg",
    "route": "oral",
    "location": "page 5, row 4"
    }}
    ]
    }}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4-0125-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        raise RuntimeError(f"Failed to extract entities using OpenAI: {e}")

def process_pdf(filepath, first_page, last_page):
    start_time = time.time()  # Start timing
    try:
        logging.info(f"Starting to process file: {filepath}")
        
        images = convert_images(filepath, first_page, last_page)
        logging.info("Image conversion complete.")
        
        text = extract_text(images)
        logging.info("Text extraction complete.")
        
        json_data_str = extract_entities(text)
        json_data = json.loads(json_data_str)  # Convert JSON string to Python dictionary
        logging.info(f"Entity extraction complete. Extracted data: {json.dumps(json_data, indent=4)}")

        # Write JSON data to a file
        with open('medications.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        logging.info("JSON data written to medications.json.")

        end_time = time.time()  # End timing
        logging.info(f"Processing completed in {end_time - start_time:.2f} seconds.")
        
        return json_data
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {"error": str(e)}

def main():
    try:
        images = convert_images()
        text = extract_text(images)
        structured_data = extract_entities(text)
        #print("Raw Extracted Data:", structured_data)  # Optional: print the raw structured data for verification
        print("Clean Extracted Data:", structured_data) 
        
    except RuntimeError as e:
        print(e)

if __name__ == "__main__":
    main()
