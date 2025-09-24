from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.cpt_rules.CPT0006A import CPT0006A


def test_CPT0006A_valid_file():
    rule = CPT0006A()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0006A_invalid_unknown():
    rule = CPT0006A()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_CPT0006A_invalid_NEN5140():
    rule = CPT0006A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NEN5140.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_CPT0006A_invalid_NEN3680():
    rule = CPT0006A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NEN3680.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
