from pathlib import Path

from app.parsers.gar_parser import GARParser
from app.rules.gar.gar6 import GAR6


def test_GAR6_valid():
    rule = GAR6()
    document_path = Path(__file__).parent / "test_files" / "GAR-valid.xml"
    contents = str.encode(open(document_path).read())
    parser = GARParser.from_string(contents)
    result = rule.apply_rule(parser)
    assert result.passed is True


def test_GAR6_invalid_quality_control_method():
    rule = GAR6()
    document_path = Path(__file__).parent / "test_files" / "GAR1.xml"
    contents = str.encode(open(document_path).read())
    parser = GARParser.from_string(contents)
    result = rule.apply_rule(parser)
    assert result.passed is False


def test_GAR6_invalid_valuation_method():
    rule = GAR6()
    document_path = Path(__file__).parent / "test_files" / "GAR2.xml"
    contents = str.encode(open(document_path).read())
    parser = GARParser.from_string(contents)
    result = rule.apply_rule(parser)
    assert result.passed is False
