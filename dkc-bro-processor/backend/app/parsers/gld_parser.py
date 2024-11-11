from typing import Any

from app.parsers.xml_parser import XmlParser


class GLDParser(XmlParser):
    OBJECT_TYPE: str = "GLD"

    def __init__(self, xml_tree: Any):
        super().__init__(xml_tree)
