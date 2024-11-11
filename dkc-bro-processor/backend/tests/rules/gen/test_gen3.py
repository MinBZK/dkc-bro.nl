from pathlib import Path

from app.parsers.cpt_parser import CPTParser
from app.rules.gen.gen3 import GEN3


def test_GEN3_valid_cpt_file():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_valid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN3_valid_gmw_file():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN3_invalid_cpt_file_WW():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_invalid.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN3_invalid_gmw_file_WW():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "gmw_rws1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN3_invalid_cpt_file_PT():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "cpt_invalid_pt.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GEN3_invalid_gmw_file_PT():
    rule = GEN3()
    document_path = Path(__file__).parent.parent / "gen" / "test_files" / "gmw_rws1_pt.xml"
    contents = str.encode(open(document_path).read())
    parser = CPTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
