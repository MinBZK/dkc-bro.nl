from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt7 import CPT7


def test_CPT7_valid_file():
    rule = CPT7()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT7_invalid_file_1():
    rule = CPT7()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT7_invalid_file_2():
    rule = CPT7()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
