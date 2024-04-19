from app.expert.parsers.xml_parser import XmlParser
from app.utils.parser_utils import (
    CORRECTION_REQUEST,
    REGISTRATION_REQUEST,
    SOURCE_DOCUMENT,
)


class BHRGT_Parser(XmlParser):
    object_type = "BHR-GT"
    request_types = [
        "BHR_GT_CompleteReport_V1",
        "BHR_GT_StartReport_V1",
        "BHR_GT_EndReport_V1",
    ]

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.determine_document_is_of_type()

    def determine_document_is_of_type(self):
        request_type = ""
        if REGISTRATION_REQUEST in self.metadata:
            request_type = REGISTRATION_REQUEST
        elif CORRECTION_REQUEST in self.metadata:
            request_type = CORRECTION_REQUEST
        if request_type:
            if SOURCE_DOCUMENT in self.metadata[request_type]:
                if any(
                    [
                        x in self.metadata[request_type][SOURCE_DOCUMENT]
                        for x in self.request_types
                    ]
                ):
                    self.is_request_of_type = True
