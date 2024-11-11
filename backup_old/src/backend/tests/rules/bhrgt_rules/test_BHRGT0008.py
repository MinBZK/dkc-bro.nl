from pathlib import Path

from app.expert.parsers.bhrgt_parser import BHRGT_Parser
from app.expert.rules.bhrgt_rules.BHRGT0008 import BHRGT0008


def test_BHRGT008_valid_file():
    rule = BHRGT0008()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_BHRGT008_invalid_file():
    rule = BHRGT0008()
    document_path = Path(__file__).parent / "test_files" / "BHR-GT1.xml"
    contents = str.encode(open(document_path).read())
    parser = BHRGT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
