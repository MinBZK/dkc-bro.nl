from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt4b import CPT4B


def test_CPT4B_valid_file():
    rule = CPT4B()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT4B_invalid_file():
    rule = CPT4B()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
