from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.gen.gen2 import GEN2


def test_GEN2_valid_cpt_file():
    rule = GEN2()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN2_valid_gmw_file():
    rule = GEN2()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN2_invalid_cpt_file():
    rule = GEN2()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_invalid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN2_invalid_gmw_file():
    rule = GEN2()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "gmw_rws1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
