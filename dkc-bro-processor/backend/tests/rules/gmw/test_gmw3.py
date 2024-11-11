from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw3 import GMW3


def test_GMW3_valid_file_tube_waterpassing():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_valid_file_tube_RTKGPS():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_valid_tube_rtkgps.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_valid_file_maaiveld_RTKGPS():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_rtkgps.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_valid_file_maaiveld_waterpassing0_2():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_waterpassing0_2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_valid_file_maaiveld_waterpassing2_4():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_waterpassing2_4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_invalid_maaiveld_file():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_invalid.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW3_invalid_tube_file():
    rule = GMW3()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_invalid_tube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
