import logging

from pydantic_settings import BaseSettings

from app import utils
from app.bhp_settings import SharedSettings, RwsBhpSettings
from app.clients import BHPClient, ManagerClient

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

shared_settings = SharedSettings()

def run_poller_for_org(org_settings: BaseSettings):
    """
    Run the poller for a specific organization, using the provided settings (with BHP credentials).
    """
    logger.info(f"Started poller for organization '{org_settings.org_code}'.")
    logger.info("Initializing clients for BHP and DKC-BRO Manager...")
    bhp = BHPClient(
        shared_settings.bhp_endpoint,
        org_settings.bhp_username,
        org_settings.bhp_token
    )
    manager = ManagerClient(shared_settings.manager_url, org_settings.org_code)

    logger.info("Fetching data from BHP...")
    bhp_projects = utils.fetch_bhp_projects(bhp)
    logger.info(f"Done. Found {len(bhp_projects)} existing BHP projects in total.\n")

    logger.info("Fetching data from DKC-BRO Manager...")
    m_project_ids, m_batch_ids = utils.fetch_manager_data(manager)
    logger.info(f"Done. Found {len(m_project_ids)} existing projects and {len(m_batch_ids)} batches in total.\n")

    logger.info("Checking for differences...")
    project_batch_pairs = utils.extract_project_batches_to_process(bhp_projects, m_batch_ids)
    if not project_batch_pairs:
        logger.info("No new project-batch combinations to process. Finished.\n")
        return
    logger.info(f"Done. Found {len(project_batch_pairs)} new project-batch combinations.")

    logger.info("Fetching new documents from BHP...")
    documents = utils.fetch_bhp_documents(bhp, bhp_projects, project_batch_pairs, org_settings.org_code)
    logger.info(f"Done. Fetched {len(documents)} documents in total.\n")

    logger.info("Starting processing of BHP documents...")
    utils.process_documents(bhp, manager, documents)
    logger.info("Finished.\n")


if __name__ == "__main__":
    # Setting per organization, imported from module `bhp_settings.py`
    # For additional organizations, create and import the settings and add them to `settings_list`
    rws_settings = RwsBhpSettings()
    settings_list = [rws_settings]

    for settings in settings_list:
        run_poller_for_org(settings)
