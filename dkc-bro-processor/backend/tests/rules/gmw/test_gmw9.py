from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw9 import GMW9


def test_GMW9_valid_file_material():
    rule = GMW9()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW9_invalid_high_file():
    rule = GMW9()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW9_invalid_low_file():
    rule = GMW9()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW9_invalid_high_low_file():
    rule = GMW9()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_high_low.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
