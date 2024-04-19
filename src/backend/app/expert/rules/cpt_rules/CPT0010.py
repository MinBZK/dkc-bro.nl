# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0010(superRule):
    __docstring = """
    Controleregel CPT0010 controleert of het Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) is ingevuld

    Document is in overtreding wanneer Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) niet is ingevuld.
    """

    __feedbackMessage = "Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) is niet ingevuld"
    __explanation = "Controleert of oppervlakte kleefmantel (frictionSleeveSurfaceArea) ingevuld is in het brondocument"
    code = "10"
    name = "Oppervlakte kleefmantel"
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
            if (doc.get_element_from_metadata("frictionSleeveSurfaceArea") is None)
            else None
        )
