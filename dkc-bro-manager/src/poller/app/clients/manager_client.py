from io import BytesIO

import requests

from app import schemas


class ManagerClient:
    """
    ManagerClient for communication with the DKC-BRO Manager (manager).
    """
    def __init__(self, url: str, org_code: str):
        self.base_url = url
        self.org_code = org_code
        self.session = requests.Session()

    def __fetch(self, url_slug: str) -> requests.Response:
        """
        Reusable method for fetching data from the manager
        """
        response = self.session.get(f"{self.base_url}/{url_slug}")
        response.raise_for_status()
        return response

    def __send(self, url_slug: str, data: dict | str| bytes, files=None) -> requests.Response:
        """
        Reusable method for sending data to the manager
        """
        response = self.session.post(f"{self.base_url}/{url_slug}", data=data, files=files)
        response.raise_for_status()
        return response

    def get_project_nrs(self) -> list[int]:
        """
        Get all existing project IDs from the manager
        """
        response = self.__fetch(f"project-nrs?org_code={self.org_code}")
        data = response.json()
        return data

    def get_levering_ids(self) -> list[str]:
        """
        Get all levering IDs from the manager
        """
        response = self.__fetch(f"batch-ids?org_code={self.org_code}")

        data = response.json()
        return data

    def send_xml_for_processing(self, document: schemas.FullDocumentInfo) -> list[schemas.ManagerResult]:
        file = BytesIO(document.content.encode("utf-8"))
        files = {'documents': (document.filename, file, 'application/xml')}
        data = document.model_dump()
        del data["content"]
        response = self.__send("process-xml", files=files, data=data)
        response.raise_for_status()
        results = response.json()["results"]
        return [schemas.ManagerResult(**result) for result in results]

    def generate_findings_report(self, batch_id: str) -> bytes:
        response = self.__fetch(f"report/{batch_id}?org_code={self.org_code}")
        return response.content
