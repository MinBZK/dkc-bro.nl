from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw10 import GMW10


def test_GMW10_valid_file_single_tube():
    rule = GMW10()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW10_invalid_file_multi_tube():
    rule = GMW10()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW10_valid_file_multi_tube():
    rule = GMW10()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile5_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
