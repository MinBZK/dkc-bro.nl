from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw7 import GMW7


def test_GMW7_invalid_file():
    rule = GMW7()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW7_valid_file():
    rule = GMW7()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW7_invalid_multitube():
    rule = GMW7()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_high_low.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
