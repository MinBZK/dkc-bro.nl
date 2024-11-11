from app.parsers.xml_parser import XmlParser


class GARParser(XmlParser):
    """
    Parser for GAR (Governmental Address Register) XML documents.
    """

    OBJECT_TYPE: str = "GAR"

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
