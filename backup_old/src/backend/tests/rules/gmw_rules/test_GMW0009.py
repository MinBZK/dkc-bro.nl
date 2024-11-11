from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0009 import GMW0009


def test_GMW0009_valid_file():
    rule = GMW0009()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0009_invalid_high_file():
    rule = GMW0009()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GMW0009_invalid_low_file():
    rule = GMW0009()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
