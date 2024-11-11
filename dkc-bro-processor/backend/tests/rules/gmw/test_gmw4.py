from pathlib import Path

from app.parsers.gmw_parser import GMWParser
from app.rules.gmw.gmw4 import GMW4


def test_GMW4_invalid_file():
    rule = GMW4()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW4_valid_file_RTKGPS0_2():
    rule = GMW4()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW4_valid_file_RTKGPS2_5():
    rule = GMW4()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_waterpassing2_4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW4_invalid_file_RTKGPS_10():
    rule = GMW4()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_waterpassing0_2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_GMW4_valid_file_tachy():
    rule = GMW4()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile_maaiveld_valid_rtkgps.xml"
    contents = str.encode(open(document_path).read())
    parser = GMWParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
