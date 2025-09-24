import requests

from app import schemas


class BHPClient:
    """
    BHPClient for communication with the Bronhouderportaal (BHP).
    """
    def __init__(self, endpoint: str, username: str, token: str):
        self.base_url = endpoint
        self.session = requests.Session()
        self.session.auth = (username, token)

    def __fetch(self, url_slug: str) -> requests.Response:
        """
        Reusable method for fetching data from the BHP
        """
        response = self.session.get(f"{self.base_url}/{url_slug}", timeout=60)
        response.raise_for_status()
        return response

    def __send(
        self,
        url_slug: str,
        data: dict | str| bytes,
        plain_text: bool = False
    ) -> requests.Response:
        """
        Reusable method for sending data to the BHP
        """
        headers = {"Content-Type": "text/plain"} if plain_text else None
        response = self.session.post(f"{self.base_url}/{url_slug}", data=data, headers=headers, timeout=120)
        response.raise_for_status()
        return response

    def get_projects(self) -> list[schemas.BhpProject]:
        """
        Get the ID and name of all project in BHP
        """
        response = self.__fetch(f"projecten")
        data = response.json()
        if not data:
            return []
        return [schemas.BhpProject(**project) for project in data]

    def load_batch_ids(self, projects: list[schemas.BhpProject]) -> list[schemas.BhpProject]:
        """
        Get all levering IDs from BHP
        """
        result = []
        for project in projects:
            response = self.__fetch(f"{project.id}/leveringen?actie=CONTROLEREN")
            batch_ids: list[str] = response.json()
            project.batch_ids = batch_ids
            result.append(project)
        return result

    def get_documents_for_batch(self, project: schemas.BhpProject, batch_id: str, org_code: str) -> list[schemas.FullDocumentInfo]:
        """
        Get metadata and content of all documents in a batch for the given project

        :return: List of dictionaries containing metadata and content of the documents,
                 to be sent to the manager.
        """
        try:
            batch_info_response = self.__fetch(f"{project.id}/leveringen/{batch_id}")
        except requests.exceptions.HTTPError as e:
            # If a deleted levering is requested, a 404 error message will follow.
            # The levering is then skipped.
            if e.response.status_code == 404:
                return []
        batch_info = schemas.BatchInfo(**batch_info_response.json()) # noqa

        documents = []
        for document in batch_info.documents:
            document_response = self.__fetch(f"{project.id}/brondocumenten/{document.id}")
            content = str(document_response.content, "utf-8")
            bhp_document = schemas.FullDocumentInfo(
                bhp_document_id=document.id,
                filename=document.filename,
                org_code=org_code,
                levering_id=batch_id,
                project_nr=project.id,
                project_naam=project.name,
                bronhouder_naam=project.authority.name,
                content=content
            )
            documents.append(bhp_document)

        return documents

    def send_document_finding(
        self,
        project_id: int,
        bhp_document_id,
        feedback_message: str,
        importance: schemas.Importance
    ):
        """
        Add finding to a document in BHP
        """
        url_slug = f"{project_id}/brondocumenten/{bhp_document_id}/{importance.value}"
        self.__send(url_slug, feedback_message, plain_text=True)

    def send_batch_findings_summary(
        self,
        project_id: int,
        batch_id: str,
        summary: str,
        importance: schemas.Importance
    ):
        """
        Add a summary of findings to a batch in BHP
        """
        url_slug = f"{project_id}/leveringen/{batch_id}/{importance.value}"
        self.__send(url_slug, summary, plain_text=True)

    def send_batch_pdf_report(self, project_id: int, batch_id: str, report: bytes):
        """
        Add a PDF report to a batch in BHP
        """
        url_slug = f"{project_id}/leveringen/{batch_id}/attachments/{batch_id}-rapportage.pdf"
        # Custom code for sending the pdf file to BHP
        response = self.session.post(
            f"{self.base_url}/{url_slug}",
            data=report,
        )
        response.raise_for_status()
        return response