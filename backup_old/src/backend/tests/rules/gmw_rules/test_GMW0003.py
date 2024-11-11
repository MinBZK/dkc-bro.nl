from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0003 import GMW0003


def test_GMW0003_valid_file():
    rule = GMW0003()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0003_invalid_maaiveld_file():
    rule = GMW0003()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GMW0003_invalid_tube_file():
    rule = GMW0003()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
