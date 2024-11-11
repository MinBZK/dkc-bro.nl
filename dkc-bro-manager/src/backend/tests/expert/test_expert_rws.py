from pathlib import Path

import pytest
from fastapi.datastructures import UploadFile

from app.expert.expert_rws import ExpertRws


def test_handle_broken_xml():
    expert = ExpertRws()
    contents = """<?xml version="1.0" standalone="yes"?>
<ns:registrationRequest xmlns:ns="http://www.broservices.nl/xsd/isgmw/1.1"
    xmlns:ns1="http://www.broservices.nl/xsd/brocommon/3.0"
    xmlns:ns2="http://www.broservices.nl/xsd/gmwcommon/1.1"
    xmlns:ns3="http://www.opengis.net/gml/3.2">
    <ns1:requestReference>N1</ns1:requestReference>
    <ns1:deliveryAccountableParty>27364178</ns1:deliveryAccountableParty>
    <ns1:qualityRegime>IMBRO/A</ns1:qualityRegime>
    <ns1:underPrivilege>ja</ns1:underPrivilege>
    <ns:sourceDocument>
        <ns:Non-Existing-Document>
        </ns:Non-Existing-Document>
    </ns:sourceDocument>
</ns:registrationRequest>"""
    findings = expert.handle_bhp_document(contents, "false.xml")
    assert len(findings) == 0


# def test_handle_bhp_document_registration_cpt():
#     expert = ExpertRws()
#     document_path = (
#         Path(__file__).parent.parent
#         / "rules"
#         / "cpt_rules"
#         / "test_files"
#         / "cpt_valid.xml"
#     )
#     contents = open(document_path).read()
#     findings = expert.handle_bhp_document(contents, "cpt_valid")
#     assert len(findings) > 0


# def test_handle_bhp_document_correction_cpt():
#     expert = ExpertRws()
#     document_path = (
#         Path(__file__).parent.parent
#         / "rules"
#         / "cpt_rules"
#         / "test_files"
#         / "cpt_correctionRequest.xml"
#     )
#     contents = open(document_path).read()
#     findings = expert.handle_bhp_document(contents, "cpt_valid")
#     assert len(findings) > 0


# def test_handle_bhp_document_correction_gmw():
#     expert = ExpertRws()
#     document_path = (
#         Path(__file__).parent.parent
#         / "rules"
#         / "gmw_rules"
#         / "test_files"
#         / "gmw_move_request.xml"
#     )
#     contents = open(document_path).read()
#     findings = expert.handle_bhp_document(contents, "gmw_move_request")
#     assert len(findings) > 0


# def test_handle_bhp_document_correction_bhrgt():
#     expert = ExpertRws()
#     document_path = (
#         Path(__file__).parent.parent
#         / "rules"
#         / "bhrgt_rules"
#         / "test_files"
#         / "BHR_GT-CorrectionRequest.xml"
#     )
#     contents = open(document_path).read()
#     findings = expert.handle_bhp_document(contents, "BHR_GT-CorrectionRequest")
#     assert len(findings) > 0


@pytest.mark.asyncio
async def test_handle_upload_registration():
    expert = ExpertRws()
    document_path = (
        Path(__file__).parent.parent
        / "rules"
        / "cpt_rules"
        / "test_files"
        / "cpt_valid.xml"
    )
    with open(document_path, "rb") as file:
        upload_file: UploadFile = UploadFile(filename="cpt_valid", file=file)
        findings = await expert.validate_documents([upload_file])
        assert len(findings) > 0


@pytest.mark.asyncio
async def test_handle_upload_correction():
    expert = ExpertRws()
    document_path = (
        Path(__file__).parent.parent
        / "rules"
        / "cpt_rules"
        / "test_files"
        / "cpt_correctionRequest.xml"
    )
    with open(document_path, "rb") as file:
        upload_file: UploadFile = UploadFile(
            filename="cpt_correctionRequest", file=file
        )
        findings = await expert.validate_documents([upload_file])
        assert len(findings) > 0
