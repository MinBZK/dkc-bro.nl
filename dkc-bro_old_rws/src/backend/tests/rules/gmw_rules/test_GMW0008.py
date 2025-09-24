from pathlib import Path

from app.expert.parsers.gmw_parser import GMW_Parser
from app.expert.rules.gmw_rules.GMW0008 import GMW0008


def test_GMW0008_valid_file_material():
    rule = GMW0008()
    document_path = (
        Path(__file__).parent / "test_files" / "gmw_testfile_invalid_tube.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0008_valid_file_stand():
    rule = GMW0008()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile2.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_GMW0008_invalid_file_glue():
    rule = GMW0008()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile3_multitube.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GMW0008_invalid_file_glue_material():
    rule = GMW0008()
    document_path = Path(__file__).parent / "test_files" / "gmw_testfile4.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None


def test_GMW0008_invalid_file_material():
    rule = GMW0008()
    document_path = Path(__file__).parent / "test_files" / "gmw_replace_request.xml"
    contents = str.encode(open(document_path).read())
    parser = GMW_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
