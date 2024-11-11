from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.gen_rules.GEN0001 import GEN0001


def test_GEN0001_valid_file():
    rule = GEN0001()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_valid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GEN0001_invalid_file():
    rule = GEN0001()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_testfile1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GEN0001_valid_no_location():
    rule = GEN0001()
    valid_wbs = "P.00000183.0002-12345678-A15-F-11-ong"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_with_brackets():
    rule = GEN0001()
    valid_wbs = "[P.00095800.0022]-[31150500]"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_no_location_1():
    rule = GEN0001()
    valid_wbs = "P.00095800-31150500"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_wbssap_8():
    rule = GEN0001()
    valid_wbs = "P.000958-31150500"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_wbssap_6():
    rule = GEN0001()
    valid_wbs = "[P.00095800.0022]-123456789"
    assert rule.check_object_id_accountable_party(valid_wbs) is False


def test_GEN0001_valid_free_text():
    rule = GEN0001()
    valid_wbs = "P.00095800-31150500-sdfersdf"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_two_free_text():
    rule = GEN0001()
    valid_wbs = "P.00095800-31150500-sdf-asde"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_no_zaaknr():
    rule = GEN0001()
    valid_wbs = "P.12345678.1234-12345678"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_id_no_zaaknr_free_text():
    rule = GEN0001()
    valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_valid_id_ong():
    rule = GEN0001()
    valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_invalid_WBS():
    rule = GEN0001()
    valid_wbs = "P1.00000183.0002-12345678-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) is False


def test_GEN0001_invalid_zaaknummer():
    rule = GEN0001()
    valid_wbs = "P.00000183.0002-123456789-A15-15.2xx-F-11-ongreference"
    assert rule.check_object_id_accountable_party(valid_wbs) is False


# def test_GEN0001_invalid_reference_RWS(): #TODO: check if this is actual because this rule has been changed
#     rule = GEN0001()
#     valid_wbs = "P.00000183.0002-12345678-A15-15.2x5-F-11-ongreference"
#     assert rule.check_object_id_accountable_party(valid_wbs) is False


# def test_GEN0001_invalid_ong(): #TODO: check if this is actual because this rule has been changes
#     rule = GEN0001()
#     valid_wbs = "P.00000183.0002-12345678-A15-15.2xx-F-11-"
#     assert rule.check_object_id_accountable_party(valid_wbs) is False


def test_GEN0001_valid_id_brackets():
    rule = GEN0001()
    valid_wbs = "[P.12345678.1234]-[12345678]-[A67-565.75-S-DKM05]-[2422-217339]"
    assert rule.check_object_id_accountable_party(valid_wbs) is True


def test_GEN0001_no_valid_id_brackets():
    rule = GEN0001()
    valid_wbs = "[1.12345678.1234]-[12345678]-[A67-565.75-S-05]-[2422-217339]"
    assert rule.check_object_id_accountable_party(valid_wbs) is False


if __name__ == "__main__":
    test_GEN0001_valid_id_brackets()
    test_GEN0001_no_valid_id_brackets()
