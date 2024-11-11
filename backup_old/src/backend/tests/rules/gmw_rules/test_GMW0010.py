from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0010 import GMW0010


def test_GMW0010_valid_file_single_tube():
    rule = GMW0010()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0010_valid_file_multi_tube():
    rule = GMW0010()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0010_invalid_file_multi_tube():
    rule = GMW0010()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile5_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
