from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt7a import CPT7A


def test_CPT7A_valid_file():
    rule = CPT7A()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT7A_invalid_class():
    rule = CPT7A()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT7A_invalid_nvt():
    rule = CPT7A()
    document_path = Path(__file__).parent / "test_files" / "cpt_NVT.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT7A_invalid_unknown():
    rule = CPT7A()
    document_path = Path(__file__).parent / "test_files" / "cpt_unknown.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
