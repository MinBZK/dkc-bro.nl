from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0004 import GMW0004


def test_GMW0004_invalid_file():
    # DGPS50tot200cm
    rule = GMW0004()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GMW0004_valid_file():
    # RTKGPS0tot2cm
    rule = GMW0004()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None
