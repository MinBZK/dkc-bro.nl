import numpy as np

from app.expert.parsers.xml_parser import XmlParser
from app.utils.parser_utils import (
    CORRECTION_REQUEST,
    REGISTRATION_REQUEST,
    SOURCE_DOCUMENT,
)


class CPT_Parser(XmlParser):
    cpt_matrix = None
    dissipation_matrices = None
    object_type = "CPT"

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.generate_matrix()
        self.determine_document_is_of_type()

    def determine_document_is_of_type(self):
        request_type = ""
        if REGISTRATION_REQUEST in self.metadata:
            request_type = REGISTRATION_REQUEST
        elif CORRECTION_REQUEST in self.metadata:
            request_type = CORRECTION_REQUEST
        if (
            request_type
            and SOURCE_DOCUMENT in self.metadata[request_type]
            and "CPT" in self.metadata[request_type][SOURCE_DOCUMENT]
        ):
            self.is_request_of_type = True

    def generate_matrix(self):
        conePenetrationTest = self.get_element_by_tag_name("conePenetrationTest")
        dissipationTests = self.get_list_of_elements_by_tag_name("dissipationTest")

        if conePenetrationTest is not None:
            values = self.get_child_element_by_tag_name(conePenetrationTest, "values")
            self.cpt_matrix = CPT_Parser.convert_data_to_matrix(values.text, 25)
        if dissipationTests is not None:
            dissMatrixList = list()
            for dissipationTest in dissipationTests:
                values = self.get_child_element_by_tag_name(dissipationTest, "values")
                matrix = CPT_Parser.convert_data_to_matrix(values.text, 5)
                dissMatrixList.append(matrix)
            self.dissipation_matrices = dissMatrixList
        return None

    def get_cpt_matrix(self):
        return self.cpt_matrix

    # list of matrices
    def get_dissipation(self):
        return self.dissipation_matrices

    def get_cpt_parameters_map(self):
        return self.get_element_from_metadata("parameters")

    @staticmethod
    def convert_data_to_matrix(data, rows):
        lines = data.split(";")
        lines = [line.split(",") for line in lines]
        lines = [line for line in lines if len(line) == rows]
        return np.array(lines, dtype=np.float64)
