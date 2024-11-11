from app.parsers.xml_parser import XmlParser


class BHRGTParser(XmlParser):
    OBJECT_TYPE: str = "BHR-GT"

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
