from app.expert.parsers.xml_parser import XmlParser
from app.utils.parser_utils import (
    CORRECTION_REQUEST,
    DELETE_REQUEST,
    REGISTRATION_REQUEST,
    REPLACE_REQUEST,
    SOURCE_DOCUMENT,
)


class GLD_Parser(XmlParser):
    object_type = "GLD"
    request_types = [
        "GLD_StartRegistration",
        "GLD_Addition",
        "GLD_Closure",
        "GLD_Complete",
    ]

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.determine_document_is_of_type()

    def determine_document_is_of_type(self):
        request_type = ""
        for request in [
            CORRECTION_REQUEST,
            DELETE_REQUEST,
            REGISTRATION_REQUEST,
            REPLACE_REQUEST,
        ]:
            if request in self.metadata:
                request_type = request
                break

        if request_type in self.metadata:
            if SOURCE_DOCUMENT in self.metadata[request_type]:
                if any(
                    [
                        x in self.metadata[request_type][SOURCE_DOCUMENT]
                        for x in self.request_types
                    ]
                ):
                    self.is_request_of_type = True
