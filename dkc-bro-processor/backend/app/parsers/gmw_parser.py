from typing import Any

from app.parsers.xml_parser import XmlParser


class GMWParser(XmlParser):
    OBJECT_TYPE: str = "GMW"

    def __init__(self, xml_tree: Any):
        super().__init__(xml_tree)
        self.object_type = self.OBJECT_TYPE
