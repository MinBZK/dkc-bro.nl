import logging

import requests.exceptions

from app.clients import BHPClient, ManagerClient
from app.schemas import BhpProject, FullDocumentInfo, DocumentWithResults, BatchSummary, Importance

logger = logging.getLogger(__name__)


def _create_project_batch_pairs(project_id: int, new_batches: set[str]):
    return [(project_id, batch_id) for batch_id in new_batches]


def _find_project(bhp_projects: list[BhpProject], project_id: int):
    return next(
        project
        for project in bhp_projects
        if project.id == project_id
    )


def extract_project_batches_to_process(
    bhp_projects: list[BhpProject],
    manager_batch_ids: list[str],
) -> list[tuple[int, str]]:
    """
    Extract the projects that are new, or have new batches
    """
    project_batch_pairs = []
    for bhp_project in bhp_projects:
        new_batches = set(bhp_project.batch_ids) - set(manager_batch_ids)
        if not new_batches:
            continue

        pairs = _create_project_batch_pairs(bhp_project.id, new_batches)
        project_batch_pairs.extend(pairs)

    return project_batch_pairs


def fetch_bhp_projects(bhp: BHPClient) -> list[BhpProject]:
    bhp_projects = bhp.get_projects()
    bhp_projects = bhp.load_batch_ids(bhp_projects)
    return bhp_projects


def fetch_manager_data(manager: ManagerClient) -> tuple[list[int], list[str]]:
    m_project_ids = manager.get_project_nrs()
    m_batch_ids = manager.get_levering_ids()
    return m_project_ids, m_batch_ids


def fetch_bhp_documents(
    bhp: BHPClient,
    bhp_projects: list[BhpProject],
    project_batch_pairs: list[tuple[int, str]],
    org_code: str
) -> list[FullDocumentInfo]:
    all_documents = []
    for project_id, batch_id in project_batch_pairs:
        logger.info(f"Retrieving docs for project {project_id} and batch {batch_id}")
        project = _find_project(bhp_projects, project_id)
        documents = bhp.get_documents_for_batch(project, batch_id, org_code)
        all_documents.extend(documents)

    return all_documents


def filter_valid_docs(documents: list[FullDocumentInfo]) -> list[FullDocumentInfo]:
    valid_docs = [doc for doc in documents if doc.content]
    n_invalid_docs = len(documents) - len(valid_docs)
    if n_invalid_docs > 0:
        logger.warning(f"Skipping {n_invalid_docs} empty document(s).")
    if len(valid_docs) > 0:
        logger.info(f"Will process {len(valid_docs)} valid document(s).")
    else:
        logger.info("No valid documents to process. Finished.")
        return []

    return valid_docs


def process_documents(bhp: BHPClient, manager: ManagerClient, documents: list[FullDocumentInfo]):
    batch_summaries: dict[str, BatchSummary] = {}
    valid_docs = filter_valid_docs(documents)
    if not valid_docs:
        logger.info("No valid documents to process.")
        return
    for doc in valid_docs:
        logger.info(f"Sending {doc.filename} to DKC-BRO manager (doc_id={doc.bhp_document_id}, batch_id={doc.levering_id}).")
        doc_with_results = send_to_manager(manager, doc)
        n_findings = len(doc_with_results.results) if doc_with_results.results else 0
        logger.info(f"Received back {n_findings} result(s).")

        batch_summaries.setdefault(
            doc_with_results.levering_id,
            BatchSummary(
                project_id=doc_with_results.project_nr,
                batch_id=doc_with_results.levering_id,
                importance_list=[],
                feedback_messages=[],
            )
        )

        logger.info(f"Sending findings of {doc.filename} to BHP.")
        importances, feedback_messages = send_document_findings_to_bhp(bhp, doc_with_results)
        batch_summaries[doc_with_results.levering_id].importance_list.extend(importances)
        batch_summaries[doc_with_results.levering_id].feedback_messages.extend(feedback_messages)
    logger.info("Finished handling od document-level findings\n")

    logger.info("Starting handling of batch summaries and reports...")
    for summary in batch_summaries.values():
        logger.info(f"Sending text summary for batch {summary.batch_id} to BHP.")
        bhp.send_batch_findings_summary(
            summary.project_id,
            summary.batch_id,
            summary.summary,
            summary.importance
        )
        logger.info(f"Sending PDF report for batch {summary.batch_id} to BHP.")
        try:
            report = manager.generate_findings_report(summary.batch_id)
            bhp.send_batch_pdf_report(summary.project_id, summary.batch_id, report)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                logger.warning(
                    f"Failed sending PDF report. "
                    f"Batch {summary.batch_id} is not found for this organization or has already been assigned to an existing organization."
                )


def send_to_manager(
    manager: ManagerClient,
    document: FullDocumentInfo
) -> DocumentWithResults:
    """
    Send Document from BHP + additional info to DKC-BRO manager for processing
    """
    manager_result = manager.send_xml_for_processing(document)
    doc_with_results = DocumentWithResults(**document.model_dump(), results=manager_result)
    return doc_with_results


def send_document_findings_to_bhp(
    bhp: BHPClient,
    doc_with_results: DocumentWithResults
) -> tuple[list[Importance], list[str]]:
    """
    Send findings on a document level to BHP.

    :returns: list of importances and list of feedback messages for further processing
    """
    importances = []
    feedback_messages = []
    for result in doc_with_results.results:
        inner_result = result.result
        feedback_message = inner_result.get("feedback_message", "") or ""
        feedback_messages.append(feedback_message)
        importances.append(result.importance)
        bhp.send_document_finding(
            doc_with_results.project_nr,
            doc_with_results.bhp_document_id,
            feedback_message,
            result.importance,
        )

    return importances, feedback_messages
