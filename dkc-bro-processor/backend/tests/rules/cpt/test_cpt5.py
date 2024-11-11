from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt5 import CPT5


def test_CPT5_valid_file():
    rule = CPT5()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT5_invalid_file():
    rule = CPT5()
    document_path = Path(__file__).parent / "test_files" / "cpt_unknown.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT5_invalid_unknown_file():
    rule = CPT5()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
