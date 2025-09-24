from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.cpt_rules.CPT0007A import CPT0007A


def test_CPT0007A_valid_file():
    rule = CPT0007A()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0007A_invalid_class():
    rule = CPT0007A()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_CPT0007A_invalid_nvt():
    rule = CPT0007A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NVT.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_CPT0007A_invalid_unknown():
    rule = CPT0007A()
    document_path = Path(__file__).parent / "test_files" / "cpt_unknown.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
