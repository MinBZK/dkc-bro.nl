from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt8a import CPT8A


def test_CPT8A_valid_file():
    rule = CPT8A()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT8A_invalid_electrical():
    rule = CPT8A()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT8A_invalid_mechanical():
    rule = CPT8A()
    document_path = Path(__file__).parent / "test_files" / "cpt_mechanical.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT8A_invalid_unknown():
    rule = CPT8A()
    document_path = Path(__file__).parent / "test_files" / "cpt_unknown.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
