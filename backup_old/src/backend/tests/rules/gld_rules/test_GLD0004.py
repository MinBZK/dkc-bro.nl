from pathlib import Path

from app.expert.parsers.gld_parser import GLD_Parser
from app.expert.rules.gld_rules.GLD0004 import GLD0004

# TODO: Make date in valid test case dynamic so that it always will fall within the last 20 days
# def test_GLD0004_valid_file():
#     rule = GLD0004()
#     document_path = (
#         Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch-valid.xml"
#     )
#     contents = str.encode(open(document_path).read())
#     parser = GLD_Parser.from_string(contents)
#     assert rule.applyRule(parser) is None


def test_GLD0004_valid_file_start_registration():
    rule = GLD0004()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GLD0004_valid_file_closure():
    rule = GLD0004()
    document_path = Path(__file__).parent / "test_files" / "GLD_StartRegistration.xml"
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GLD0004_invalid_file():
    rule = GLD0004()
    document_path = (
        Path(__file__).parent / "test_files" / "GLD_Addition_sensorisch1.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GLD_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
