# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0008(superRule):
    __docstring = """
    Controleregel CPT0008 controleert of het Domein Sondeermethode (cptMethod) is ingevuld met mechanischContinu of mechanischDiscontinu.
    Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

    Document is in overtreding wanneer Domein Sondeermethode (cptMethod) is ingevuld met mechanischContinu of mechanischDiscontinu.
    """

    __feedbackMessage = "Domein Sondeermethode (cptMethod) is ingevuld met mechanischContinu of mechanischDiscontinu. Vraag na bij een adviseur of dit geschikt is voor dit project."
    __explanation = "Controleert of het Domein Sondeermethode (cptMethod) gevuld is met mechanischContinu of mechanischDiscontinu. Als dit zo is moet er navraag gedaan worden bij een adviseur."
    code = "8"
    name = "Domein Sondeermethode (BRO) mechanischContinu of mechanischDiscontinu"
    object_type = "CPT"
    invalid_cpt_methods = [
        "mechanischContinu",
        "mechanischDiscontinu",
        # "elektrisch",
        # "mechanisch",
        # "onbekend",
    ]

    def __init__(self, emergence=enums.Importance.INFO):
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
        return (
            self.getFeedbackMessage()
            if (doc.get_element_from_metadata("cptMethod") in self.invalid_cpt_methods)
            else None
        )
