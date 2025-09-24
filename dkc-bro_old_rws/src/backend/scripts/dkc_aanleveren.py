import requests
import os
import logging
import base64
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BronhouderportaalClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Environment variables for authentication and URL
        self.username = os.environ.get("BHP-USERNAME")
        self.password = os.environ.get("BHP-TOKEN")
        self.base_url = os.environ.get("BHP-ENDPOINT")

        # Log the loaded environment variables for debugging
        logger.info(f"Loaded environment variables: BHP-USERNAME={self.username}, BHP-ENDPOINT={self.base_url}")

        # Check if any environment variable is missing
        if not self.username or not self.password or not self.base_url:
            logger.error("One or more environment variables are missing. Please check your .env file.")
            raise ValueError("Missing environment variables")

        # Encode the username and password in Base64
        auth_string = f"{self.username}:{self.password}"
        auth_bytes = auth_string.encode('utf-8')
        self.auth_base64 = base64.b64encode(auth_bytes).decode('utf-8')

    def upload_brondocument(self, projectnummer, xml_file_path, filename):
        # URL for the POST request
        url = f"{self.base_url}/{projectnummer}/leveringen"
        logger.info(url)

        # Headers for the request
        headers = {
            "Content-Type": "application/xml",
            "Authorization": f"Basic {self.auth_base64}"
        }

        # Read the XML file content
        try:
            with open(xml_file_path, 'r') as file:
                xml_payload = file.read()
        except FileNotFoundError:
            logger.error(f"XML file not found: {xml_file_path}")
            return

        # Parameters for the request
        params = {
            "filename": filename
        }

        # Make the POST request
        response = requests.post(url, headers=headers, params=params, data=xml_payload)

        # Check the response
        if response.status_code == 201:
            logger.info("Brondocument successfully uploaded.")
            logger.info(f"Response: {response.json()}")
        else:
            logger.error(f"Failed to upload brondocument. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")

    def add_info_note(self, projectnummer, levering_identifier, note):
        # URL for the POST request
        url = f"{self.base_url}/{projectnummer}/leveringen/{levering_identifier}/info"
        logger.info(url)

        # Headers for the request
        headers = {
            "Content-Type": "text/plain",
            "Authorization": f"Basic {self.auth_base64}"
        }

        # Make the POST request
        response = requests.post(url, headers=headers, data=note)

        # Check the response
        if response.status_code == 204:
            logger.info("Info note successfully added.")
        elif response.status_code == 401:
            logger.error("Authentication problem. Status code: 401")
        elif response.status_code == 403:
            logger.error("Authorization problem. Status code: 403")
        elif response.status_code == 404:
            logger.error("Resource not found. Status code: 404")
        else:
            logger.error(f"Failed to add info note. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")

    def add_attachment(self, projectnummer, brondocument_id, filename, attachment_path):
        # URL for the POST request
        url = f"{self.base_url}/{projectnummer}/brondocumenten/{brondocument_id}/attachments/{filename}"
        logger.info(url)

        # Headers for the request
        headers = {
            "Content-Type": "application/octet-stream",
            "Authorization": f"Basic {self.auth_base64}"
        }

        # Read the attachment file content
        try:
            with open(attachment_path, 'rb') as file:
                attachment_payload = file.read()
        except FileNotFoundError:
            logger.error(f"Attachment file not found: {attachment_path}")
            return

        # Make the POST request
        response = requests.post(url, headers=headers, data=attachment_payload)

        # Check the response
        if response.status_code == 204:
            logger.info("Attachment successfully added.")
        elif response.status_code == 401:
            logger.error("Authentication problem. Status code: 401")
        elif response.status_code == 403:
            logger.error("Authorization problem. Status code: 403")
        elif response.status_code == 404:
            logger.error("Resource not found. Status code: 404")
            logger.error(f"Response: {response.text}")
        else:
            logger.error(f"Failed to add attachment. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")

if __name__ == "__main__":
    client = BronhouderportaalClient()
    
    # Example usage
    client.upload_brondocument(projectnummer=1954, xml_file_path="CPT1_original.xml", filename="brondocument-cpt1-original.xml")
    client.add_info_note(projectnummer=408, levering_identifier="0000000180", note="This is an info note again.")
    client.add_attachment(projectnummer=408, brondocument_id="0000000180", filename="0000000180-rapportage.pdf", attachment_path="0001240558.pdf")