from pathlib import Path

from app.parsers.gld_parser import GLDParser
from app.rules.gld.gld6 import GLD6


def test_GLD6_valid_file_start_registration():
    rule = GLD6()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD6_valid_file_closure():
    rule = GLD6()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD6_invalid_file():
    rule = GLD6()
    document_path = Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch1.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
