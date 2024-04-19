from pathlib import Path

from app.expert.parsers.bhrgt_parser import BHRGT_Parser
from app.expert.rules.bhrgt_rules.BHRGT0007 import BHRGT0007


def test_BHRGT0007_valid_file():
    rule = BHRGT0007()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_BHRGT0007_invalid_file():
    rule = BHRGT0007()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT1.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
