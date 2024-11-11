# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0013(superRule):
    __docstring = """
    Controleregel CPT0012 controleert of het Sondeerapparaat Conusdiameter (coneDiameter) is ingevuld

    Document is in overtreding wanneer Sondeerapparaat Conusdiameter (coneDiameter) niet is ingevuld.
    """

    __feedbackMessage = "Sondeerapparaat Conusdiameter (coneDiameter) is niet ingevuld"
    __explanation = (
        "Controleert of conusdiameter (coneDiameter) ingevuld is in het brondocument"
    )
    code = "13"
    name = "Conusdiameter"
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
            if (doc.get_element_from_metadata("coneDiameter") is None)
            else None
        )
