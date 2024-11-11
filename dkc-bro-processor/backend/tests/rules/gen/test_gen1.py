from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.gen.gen1 import GEN1


def test_GEN1_valid_file():
    rule = GEN1()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN1_invalid_file():
    rule = GEN1()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
