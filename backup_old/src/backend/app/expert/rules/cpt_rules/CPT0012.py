# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0012(superRule):
    __docstring = """
    Controleregel CPT0012 controleert of het Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) is ingevuld

    Document is in overtreding wanneer Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) niet is ingevuld.
    """

    __feedbackMessage = "Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) is niet ingevuld"
    __explanation = "Controleert of element conuspunt (coneSurfaceQuotient) ingevuld is in het brondocument"
    code = "12"
    name = "Oppervlaktequotient conuspunt"
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
            if (doc.get_element_from_metadata("coneSurfaceQuotient") is None)
            else None
        )
