from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0006 import GMW0006


def test_GMW0006_valid_file():
    rule = GMW0006()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0006_invalid_file():
    rule = GMW0006()
    document_path = Path(__file__).parent / "test_files" / "gmw_rws1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
