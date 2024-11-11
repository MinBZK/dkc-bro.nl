from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt8 import CPT8


def test_CPT8_valid_file():
    rule = CPT8()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT8_invalid_discontinu():
    rule = CPT8()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT8_invalid_continu():
    rule = CPT8()
    document_path = Path(__file__).parent / "test_files" / "cpt_invalid_continu.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
