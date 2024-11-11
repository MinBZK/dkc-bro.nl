from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw6 import GMW6


def test_GMW6_valid_file():
    rule = GMW6()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW6_invalid_file():
    rule = GMW6()
    document_path = Path(__file__).parent / "test_files" / "gmw_rws1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
