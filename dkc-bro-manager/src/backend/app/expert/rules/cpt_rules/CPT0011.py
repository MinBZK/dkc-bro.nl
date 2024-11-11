# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0011(superRule):
    __docstring = """
    Controleregel CPT0011 controleert of het Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) is ingevuld

    Document is in overtreding wanneer Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) niet is ingevuld.
    """

    __feedbackMessage = "Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) is niet ingevuld"
    __explanation = "Controleert of afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) aanwezig is in het brondocument"
    code = "011"
    name = "Afstand conus to midden kleefmantel"
    object_type = "CPT"

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
            if (doc.get_element_from_metadata("coneToFrictionSleeveDistance") is None)
            else None
        )
