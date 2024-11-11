from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt6a import CPT6A


def test_CPT6A_valid_file():
    rule = CPT6A()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT6A_invalid_unknown():
    rule = CPT6A()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT6A_invalid_NEN5140():
    rule = CPT6A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NEN5140.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT6A_invalid_NEN3680():
    rule = CPT6A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NEN3680.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
