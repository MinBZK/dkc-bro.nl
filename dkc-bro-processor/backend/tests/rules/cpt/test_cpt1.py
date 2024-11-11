from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.cpt.cpt1 import CPT1


def test_CPT1_valid_file():
    rule = CPT1()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_CPT1_invalid_file():
    rule = CPT1()
    document_path = Path(__file__).parent / "test_files" / "cpt_rws1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
