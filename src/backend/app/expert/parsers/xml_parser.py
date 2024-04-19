import re
from abc import ABC, abstractmethod

from lxml import etree


class XmlParser(ABC):
    ns_map = {}
    metadata = {}
    is_request_of_type = False
    object_type = ""

    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.generate_ns_map()
        self.metadata = XmlParser.lxml_to_dict(self.get_root())

    def get_object_type(self):
        return self.object_type

    def is_of_type(self):
        return self.is_request_of_type

    def get_root(self):
        if hasattr(self.xml_tree, "getroot"):
            return self.xml_tree.getroot()
        return self.xml_tree

    def get_tag(self, full_tag):
        (ns, tag) = full_tag.strip().split(":")
        if ns in self.ns_map:
            return self.ns_map[ns] + tag
        return None

    def get_element_by_tag(self, tag):
        for _, elem in etree.iterwalk(
            self.xml_tree, events=("end",), tag=self.getTag(tag)
        ):
            return elem
        return None

    # returns first element without ns matching the name param
    def get_element_by_tag_name(self, name):
        for _, elem in etree.iterwalk(self.get_root(), events=("end",)):
            if name == XmlParser.strip_ns_from_tag_name(elem.tag):
                return elem
        return None

    # returns list of elements without ns matching the name param
    def get_list_of_elements_by_tag_name(self, name):
        list_of_elements = list()
        for _, elem in etree.iterwalk(self.xml_tree, events=("end",)):
            if name == XmlParser.strip_ns_from_tag_name(elem.tag):
                list_of_elements.append(elem)
        if len(list_of_elements) != 0:
            return list_of_elements
        return None

    def get_element_from_metadata(self, name, d=None):
        if d is None:
            d = self.metadata
        for key, item in d.items():
            if key == name:
                return item
            if isinstance(item, dict):
                optional = self.get_element_from_metadata(name, item)
                if optional is not None:
                    return optional
        return None

    def generate_ns_map(self):
        for _, elem in etree.iterwalk(self.xml_tree, events=("start-ns",)):
            ns, url = elem
            self.ns_map[ns] = "{" + url + "}"

    @abstractmethod
    def determine_document_is_of_type(self):
        raise NotImplementedError

    @classmethod
    def from_string(cls, xmlString):
        return cls(etree.fromstring(xmlString))

    @classmethod
    def from_file(cls, xmlFile):
        return cls(etree.parse(xmlFile))

    # from lxml_to_dict,
    # slightly adjusted the implementation to remove some tags
    @staticmethod
    def lxml_to_dict(element):
        ret = {}
        if element.getchildren() == []:
            tag = XmlParser.strip_ns_from_tag_name(element.tag)
            if tag != "values":
                ret[tag] = element.text
        else:
            count = {}
            for elem in element.getchildren():
                subdict = XmlParser.lxml_to_dict(elem)
                tag = XmlParser.strip_ns_from_tag_name(element.tag)
                subtag = XmlParser.strip_ns_from_tag_name(elem.tag)
                # subtag can only be None if the element tag is not a String
                # (could be a comment),
                # in which case we don't add it to the dict
                if subtag is None:
                    continue
                if ret.get(tag, False) and subtag in ret[tag].keys():
                    count[subtag] = count[subtag] + 1 if count.get(subtag, False) else 1
                    elemtag = subtag + str(count[subtag])
                    subdict = {elemtag: subdict[subtag]}
                if ret.get(tag, False):
                    ret[tag].update(subdict)
                else:
                    ret[tag] = subdict
        return ret

    @staticmethod
    def get_child_element_by_tag_name(elem, name):
        for _, elem in etree.iterwalk(elem, events=("end",)):
            if name == XmlParser.strip_ns_from_tag_name(elem.tag):
                return elem
        return None

    @staticmethod
    def get_child_elements_by_tag_name(elem, name):
        for _, elem in etree.iterwalk(elem, events=("end",)):
            if name == XmlParser.strip_ns_from_tag_name(elem.tag):
                yield elem
        return None

    @staticmethod
    def strip_ns_from_tag_name(name):
        if isinstance(name, str):
            return re.sub("{.*}", "", name)
        return None
