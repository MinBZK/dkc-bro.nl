from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gen_rules.GEN0003 import GEN0003


def test_GEN0003_valid_cpt_file():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_valid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GEN0003_valid_gmw_file():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "gmw_rules" / "test_files" / "gmw_testfile1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GEN0003_invalid_gmw_file_WW():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "gmw_rules" / "test_files" / "gmw_rws1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GEN0003_invalid_cpt_file_WW():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_invalid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GEN0003_invalid_gmw_file_PT():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "gmw_rules" / "test_files" / "gmw_rws1_pt.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GEN0003_invalid_cpt_file_PT():
    rule = GEN0003()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_invalid_pt.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
