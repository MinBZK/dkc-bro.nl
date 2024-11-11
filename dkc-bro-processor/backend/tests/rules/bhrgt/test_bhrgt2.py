from pathlib import Path

from app.parsers.bhrgt_parser import BHRGTParser
from app.rules.bhrgt.bhrgt2 import BHR_GT2


def test_BHRGT2_valid_file():
    rule = BHR_GT2()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_BHRGT2_invalid_file_empty_date():
    rule = BHR_GT2()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT1.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)


def test_BHRGT2_invalid_file_no_date():
    rule = BHR_GT2()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT2.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGTParser.from_string(contents)
    result = rule.apply_rule(parser)
    rule.assert_result(result)
