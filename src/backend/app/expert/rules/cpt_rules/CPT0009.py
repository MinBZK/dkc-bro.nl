# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0009(superRule):
    __docstring = """
    Controleregel CPT0009 controleert of het Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) is ingevuld

    Document is in overtreding wanneer Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) niet is ingevuld.
    """

    __feedbackMessage = "Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) is niet ingevuld"
    __explanation = "Controleert of oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) ingevuld is in het brondocument"
    code = "9"
    name = "Oppervlaktequotient kleefmantel"
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
            if (doc.get_element_from_metadata("frictionSleeveSurfaceQuotient") is None)
            else None
        )
