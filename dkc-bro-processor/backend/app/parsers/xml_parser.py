import re
from abc import ABC
from typing import Any, Dict, List, Optional

from lxml import etree  # type: ignore


class XmlParser(ABC):
    def __init__(self, xml_tree: etree._Element):
        self.xml_tree = xml_tree
        self.ns_map: Dict[str, str] = {}
        self.generate_ns_map()
        self.metadata: Dict[str, Any] = self.lxml_to_dict(self.get_root())
        self.is_request_of_type: bool = False
        self.object_type: str = ""

    def get_object_type(self) -> str:
        return self.object_type

    def is_of_type(self) -> bool:
        return self.is_request_of_type

    def get_root(self) -> etree._Element:
        if hasattr(self.xml_tree, "getroot"):
            return self.xml_tree.getroot()
        return self.xml_tree

    def get_tag(self, full_tag: str) -> Optional[str]:
        ns, tag = full_tag.strip().split(":")
        return f"{self.ns_map.get(ns, '')}{tag}"

    def get_element_by_tag(self, tag: str) -> Optional[etree._Element]:
        return next(
            (elem for _, elem in etree.iterwalk(self.xml_tree, events=("end",), tag=self.get_tag(tag))),
            None,
        )

    def get_element_by_tag_name(self, name: str) -> Optional[etree._Element]:
        return next(
            (elem for _, elem in etree.iterwalk(self.get_root(), events=("end",)) if name == self.strip_ns_from_tag_name(elem.tag)),
            None,
        )

    def get_list_of_elements_by_tag_name(self, name: str) -> Optional[List[etree._Element]]:
        elements = [elem for _, elem in etree.iterwalk(self.xml_tree, events=("end",)) if name == self.strip_ns_from_tag_name(elem.tag)]
        return elements if elements else None

    def get_element_from_metadata(self, name: str, d: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        if d is None:
            d = self.metadata
        for key, item in d.items():
            if key == name:
                return item
            if isinstance(item, dict):
                result = self.get_element_from_metadata(name, item)
                if result is not None:
                    return result
        return None

    def generate_ns_map(self) -> None:
        self.ns_map = {ns: f"{{{url}}}" for ns, url in etree.iterwalk(self.xml_tree, events=("start-ns",))}

    @classmethod
    def from_string(cls, xml_string: bytes):
        return cls(etree.fromstring(xml_string, parser=etree.XMLParser()))

    @classmethod
    def from_file(cls, xml_file: str):
        return cls(etree.parse(xml_file, parser=etree.XMLParser()))

    @staticmethod
    def lxml_to_dict(element: etree._Element) -> Dict[str, Any]:
        if not element.getchildren():
            tag = XmlParser.strip_ns_from_tag_name(element.tag)
            return {tag: element.text} if tag and tag != "values" else {}

        result: Dict[str, Any] = {}
        for elem in element.getchildren():
            subdict = XmlParser.lxml_to_dict(elem)
            tag = XmlParser.strip_ns_from_tag_name(element.tag)
            subtag = XmlParser.strip_ns_from_tag_name(elem.tag)

            if not tag or not subtag:
                continue

            if tag in result and isinstance(result[tag], dict) and subtag in result[tag]:
                count = sum(1 for key in result[tag] if isinstance(key, str) and key.startswith(subtag))
                elemtag = f"{subtag}{count + 1}"
                subdict = {elemtag: subdict[subtag]}

            if tag in result:
                if isinstance(result[tag], dict):
                    result[tag].update(subdict)
                else:
                    result[tag] = [result[tag], subdict]
            else:
                result[tag] = subdict

        return result

    @staticmethod
    def strip_ns_from_tag_name(name: Optional[str]) -> Optional[str]:
        if isinstance(name, str):
            return re.sub(r"{.*}", "", name) or None
        return None

    @staticmethod
    def get_child_element_by_tag_name(elem: etree._Element, name: str) -> Optional[etree._Element]:
        return next(
            (child for _, child in etree.iterwalk(elem, events=("end",)) if name == XmlParser.strip_ns_from_tag_name(child.tag)),
            None,
        )

    @staticmethod
    def get_child_elements_by_tag_name(elem: etree._Element, name: str) -> List[etree._Element]:
        return [child for _, child in etree.iterwalk(elem, events=("end",)) if name == XmlParser.strip_ns_from_tag_name(child.tag)]
