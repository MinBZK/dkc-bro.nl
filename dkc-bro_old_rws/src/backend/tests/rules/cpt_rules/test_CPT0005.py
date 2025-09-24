from pathlib import Path

from app.expert.parsers.cpt_parser import CPT_Parser
from app.expert.rules.cpt_rules.CPT0005 import CPT0005


def test_CPT0005_valid_file_bezwijkrisico():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_bezwijkrisico.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_conusweerstand():
    rule = CPT0005()
    document_path = (
        Path(__file__).parent / "test_files" / "cpt_valid_conusweerstand.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_einddiepte():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_einddiepte.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_hellingshoek():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_hellingshoek.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_obstakel():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_obstakel.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_storing():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_storing.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_waterspanning():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_waterspanning.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_wegdrukkracht():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_valid_wegdrukkracht.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_valid_file_wrijvingsweerstand():
    rule = CPT0005()
    document_path = (
        Path(__file__).parent / "test_files" / "cpt_valid_wrijvingsweerstand.xml"
    )
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is None


def test_CPT0005_invalid_file():
    rule = CPT0005()
    document_path = Path(__file__).parent / "test_files" / "cpt_testfile1.xml"
    contents = str.encode(open(document_path).read())
    parser = CPT_Parser.from_string(contents)
    assert rule.applyRule(parser) is not None
