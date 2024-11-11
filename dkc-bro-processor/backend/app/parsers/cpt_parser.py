from typing import Any, List, Optional

import numpy as np

from app.parsers.xml_parser import XmlParser


class CPTParser(XmlParser):
    """Parser for Cone Penetration Test (CPT) XML documents."""

    OBJECT_TYPE: str = "CPT"

    def __init__(self, xml_tree):
        super().__init__(xml_tree)
        self.cpt_matrix: Optional[np.ndarray] = None
        self.dissipation_matrices: Optional[List[Optional[np.ndarray]]] = None
        self._generate_matrix()

    def _generate_matrix(self) -> None:
        """Generate CPT and dissipation matrices from XML data."""
        self._generate_cpt_matrix()
        self._generate_dissipation_matrices()

    def _generate_cpt_matrix(self) -> None:
        """Generate CPT matrix from XML data."""
        cone_penetration_test = self.get_element_by_tag_name("conePenetrationTest")
        if cone_penetration_test is not None:
            values = self.get_child_element_by_tag_name(cone_penetration_test, "values")
            if values is not None:
                self.cpt_matrix = self.convert_data_to_matrix(values.text, 25)

    def _generate_dissipation_matrices(self) -> None:
        """Generate dissipation matrices from XML data."""
        dissipation_tests = self.get_list_of_elements_by_tag_name("dissipationTest")
        if dissipation_tests:
            self.dissipation_matrices = []
            for test in dissipation_tests:
                values_element = self.get_child_element_by_tag_name(test, "values")
                if values_element is not None and values_element.text:
                    matrix = self.convert_data_to_matrix(values_element.text, 5)
                else:
                    matrix = None
                self.dissipation_matrices.append(matrix)
        else:
            self.dissipation_matrices = None

    def get_cpt_matrix(self) -> Optional[np.ndarray]:
        """Get the CPT matrix."""
        return self.cpt_matrix

    def get_dissipation(self) -> Optional[List[Optional[np.ndarray]]]:
        """Get the list of dissipation matrices."""
        return self.dissipation_matrices

    def get_cpt_parameters_map(self) -> Any | None:
        """Get the CPT parameters map from metadata."""
        return self.get_element_from_metadata("parameters")

    @staticmethod
    def convert_data_to_matrix(data: str, rows: int) -> np.ndarray:
        """Convert string data to a numpy matrix."""
        lines = [line.split(",") for line in data.split(";") if len(line.split(",")) == rows]
        return np.array(lines, dtype=np.float64)
