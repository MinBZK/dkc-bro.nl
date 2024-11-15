# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0008A(superRule):
    __docstring = """
    Controleregel CPT0008A controleert of het Domein Sondeermethode (cptMethod) is ingevuld met elektrisch, mechanisch of onbekend.

    Document is in overtreding wanneer Domein Sondeermethode (cptMethod)  is ingevuld met elektrisch, mechanisch of onbekend.
    """

    __feedbackMessage = "Domein Sondeermethode (cptMethod) is ingevuld met een niet geldige waarde: '%s'."
    __explanation = "Controleert of het Domein Sondeermethode (cptMethod) gevuld is met elektrisch, mechanisch of onbekend. Als dit zo is moet er gerouterneerd worden."
    code = "08A"
    name = "Domein Sondeermethode (BRO) elektrisch, mechanisch of onbekend"
    object_type = "CPT"
    invalid_cpt_methods = [
        "elektrisch",
        "mechanisch",
        "onbekend",
    ]

    def __init__(self, emergence=enums.Importance.ERROR):
        super().__init__(
            self.code,
            self.name,
            self.object_type,
            emergence,
            self.__feedbackMessage,
            self.__explanation,
            self.__docstring,
        )

    def applyRule(self, doc):
        cpt_method = doc.get_element_from_metadata("cptMethod")
        if cpt_method in self.invalid_cpt_methods:
            return self.getFeedbackMessage() % cpt_method
        else:
            return None
