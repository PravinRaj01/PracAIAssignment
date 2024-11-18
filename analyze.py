from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from dotenv import load_dotenv
import time
import os

# Load environment variables from .env file
load_dotenv("pracAI.env")

# Retrieve the subscription key and endpoint from environment variables
endpoint = os.getenv("ENDPOINT")
key = os.getenv("KEY")

# Initialize the client with the credentials
credentials = CognitiveServicesCredentials(key)
client = ComputerVisionClient(endpoint=endpoint, credentials=credentials)

def read_image(uri):
    try:
        # Send the image URI for OCR analysis
        raw_response = client.read(uri, raw=True)
        operation_location = raw_response.headers["Operation-Location"]
        operation_id = operation_location.split("/")[-1]

        # Poll the API until the OCR operation completes
        max_retries = 10
        for _ in range(max_retries):
            result = client.get_read_result(operation_id)
            if result.status not in ['notStarted', 'running']:
                break
            time.sleep(1)

        # Check the result and extract text if successful
        if result.status == OperationStatusCodes.succeeded:
            # Join all lines of text
            text = " ".join(
                line.text for read_result in result.analyze_result.read_results for line in read_result.lines
            )
            # Clean text: Remove unwanted characters like the middle dot
            cleaned_text = text.replace("\u00b7", "").strip()
            return cleaned_text or "No text found"
        else:
            return "Error: OCR operation failed"
    except Exception as e:
        return f"Error during image analysis: {e}"

