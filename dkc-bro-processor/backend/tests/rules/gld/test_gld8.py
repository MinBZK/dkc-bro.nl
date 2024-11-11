from pathlib import Path

from app.parsers.gld_parser import GLDParser
from app.rules.gld.gld8 import GLD8


def test_GLD8_valid_file():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD8_valid_file_closure():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD8_valid_file_start_registration():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD8_valid_file_controle_meting():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_Addition_controleMeting.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD8_invalid_file():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch1.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GLD8_invalid_volledig_beoordeeld():
    rule = GLD8()
    document_path = Path(__file__).parent / "test_files" / "GLD_Addition_volledigBeoordeeld.xml"
    contents = str.encode(open(document_path).read())
    parser = GLDParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
