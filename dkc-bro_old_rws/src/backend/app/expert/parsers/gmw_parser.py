from app.expert.parsers.xml_parser import XmlParser
from app.utils.parser_utils import REGISTRATION_REQUEST, SOURCE_DOCUMENT


class GMW_Parser(XmlParser):
    object_type = "GMW"
    correction_types = [
        "replaceRequest",
        "insertRequest",
        "moveRequest",
        "deleteRequest",
    ]
    request_types = ["GMW_Construction", "GMW_ConstructionWithHistory"]

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.determine_document_is_of_type()

    def determine_document_is_of_type(self):
        if REGISTRATION_REQUEST in self.metadata:
            if SOURCE_DOCUMENT in self.metadata[REGISTRATION_REQUEST]:
                if any(
                    [
                        x in self.metadata[REGISTRATION_REQUEST][SOURCE_DOCUMENT]
                        for x in self.request_types
                    ]
                ):
                    self.is_request_of_type = True
        else:
            correction_type = ""
            for correction in self.correction_types:
                if correction in self.metadata:
                    correction_type = correction
                    break
            if correction_type and any(
                [
                    x in self.metadata[correction_type][SOURCE_DOCUMENT]
                    for x in self.request_types
                ]
            ):
                self.is_request_of_type = True
