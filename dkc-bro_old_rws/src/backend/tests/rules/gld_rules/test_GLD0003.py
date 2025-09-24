from pathlib import Path

from app.expert.parsers.gld_parser import GLD_Parser
from app.expert.rules.gld_rules.GLD0003 import GLD0003


def test_GLD0003_valid_file():
    rule = GLD0003()
    document_path = (
        Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch-valid.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GLD0003_valid_file_start_registration():
    rule = GLD0003()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GLD0003_valid_file_closure():
    rule = GLD0003()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GLD0003_invalid_file():
    rule = GLD0003()
    document_path = (
        Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
