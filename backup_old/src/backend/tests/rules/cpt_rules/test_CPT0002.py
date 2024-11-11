from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.cpt_rules.CPT0002 import CPT0002


def test_CPT0002_invalid_file():
    rule = CPT0002()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_CPT0002_valid_file():
    rule = CPT0002()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None
