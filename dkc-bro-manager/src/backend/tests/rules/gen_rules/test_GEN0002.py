from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gen_rules.GEN0002 import GEN0002


def test_GEN0002_valid_cpt_file():
    rule = GEN0002()
    document_path = (
        Path(__file__).parent.parent / "cpt_rules" / "test_files" / "cpt_valid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GEN0002_valid_gmw_file():
    rule = GEN0002()
    document_path = (
        Path(__file__).parent.parent / "gmw_rules" / "test_files" / "gmw_testfile1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GEN0002_invalid_gmw_file():
    rule = GEN0002()
    document_path = (
        Path(__file__).parent.parent / "gmw_rules" / "test_files" / "gmw_rws1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
