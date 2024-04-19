from pathlib import Path

from app.expert.parsers.bhrgt_parser import BHRGT_Parser
from app.expert.rules.bhrgt_rules.BHRGT0002 import BHRGT0002


def test_BHRGT0002_valid_file():
    rule = BHRGT0002()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_BHRGT0002_invalid_file_empty_date():
    rule = BHRGT0002()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT1.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_BHRGT0002_invalid_file_no_date():
    rule = BHRGT0002()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT2.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
