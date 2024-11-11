from pathlib import Path

from app.expert.parsers.gar_parser import GAR_Parser
from app.expert.rules.gar_rules.GAR0006 import GAR0006


def test_GAR0006_valid():
    rule = GAR0006()
    document_path = Path(__file__).parent / "test_files" / "GAR-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = GAR_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GAR0006_invalid_quality_control_method():
    rule = GAR0006()
    document_path = Path(__file__).parent / "test_files" / "GAR1.xml"
    contents = str.encode(open(document_path).read())
    parser = GAR_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GAR0006_invalid_valuation_method():
    rule = GAR0006()
    document_path = Path(__file__).parent / "test_files" / "GAR2.xml"
    contents = str.encode(open(document_path).read())
    parser = GAR_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
