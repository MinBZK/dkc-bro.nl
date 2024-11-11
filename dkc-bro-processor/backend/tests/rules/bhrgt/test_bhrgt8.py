from pathlib import Path

from app.parsers.bhrgt_parser import BHRGTParser
from app.rules.bhrgt.bhrgt8 import BHR_GT8


def test_BHRGT8_valid_file():
    rule = BHR_GT8()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_BHRGT8_invalid_unknown():
    rule = BHR_GT8()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT1.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_BHRGT8_invalid_empty():
    rule = BHR_GT8()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-empty.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_BHRGT8_invalid_whitespace():
    rule = BHR_GT8()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-whitespace.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
