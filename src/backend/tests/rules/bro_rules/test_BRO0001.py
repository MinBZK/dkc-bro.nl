from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.bro_rules.BRO0001 import BRO0001


def test_BRO0001_valid_file():
    rule = BRO0001()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_valid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_BRO0001_invalid_file():
    rule = BRO0001()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_testfile1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_BRO0001_valid_no_location():
    rule = BRO0001()
    valid_wbs = "P.00000183.0002-12345678-A15-F-11-ong"
    assert rule.check_object_id_accountable_party(valid_wbs) == True


def test_BRO0001_valid_id_no_ong():
    rule = BRO0001()
    valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11"
    assert rule.check_object_id_accountable_party(valid_wbs) == True


def test_BRO0001_valid_id_ong():
    rule = BRO0001()
    valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) == True


def test_BRO0001_invalid_WBS():
    rule = BRO0001()
    valid_wbs = "P1.00000183.0002-12345678-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) == False


def test_BRO0001_invalid_zaaknummer():
    rule = BRO0001()
    valid_wbs = "P.00000183.0002-123456789-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) == False


# def test_BRO0001_invalid_reference_RWS(): #TODO: check if this is actual because this rule has been changes
#     rule = BRO0001()
#     valid_wbs = "P.00000183.0002-12345678-A15-15.2x5-F-11-ongreference"
#     assert rule.check_object_id_accountable_party(valid_wbs) == False


# def test_BRO0001_invalid_ong(): #TODO: check if this is actual because this rule has been changes
#     rule = BRO0001()
#     valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11-"
#     assert rule.check_object_id_accountable_party(valid_wbs) == False


def test_BRO0001_valid_id_brackets():
    rule = BRO0001()
    valid_wbs = "[P.12345678.1234]-[12345678]-[A67-565.75-S-DKM05]-[2422-217339]"
    assert rule.check_object_id_accountable_party(valid_wbs) == True


def test_BRO0001_no_valid_id_brackets():
    rule = BRO0001()
    valid_wbs = "[1.12345678.1234]-[12345678]-[A67-565.75-S-05]-[2422-217339]"
    assert rule.check_object_id_accountable_party(valid_wbs) == False


if __name__ == "__main__":
    test_BRO0001_valid_id_brackets()
    test_BRO0001_no_valid_id_brackets()
