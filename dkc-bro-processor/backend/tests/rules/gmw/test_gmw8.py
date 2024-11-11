from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw8 import GMW8


def test_GMW8_valid_file_material():
    rule = GMW8()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_invalid_tube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW8_valid_file_stand():
    rule = GMW8()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW8_invalid_file_glue():
    rule = GMW8()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW8_invalid_file_material_glue():
    rule = GMW8()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW8_invalid_material_file():
    rule = GMW8()
    document_path = Path(__file__).parent / "test_files" / "gmw_replace_request.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
