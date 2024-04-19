# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0006(superRule):
    __docstring = """
    Controleregel GMW0006 controleert of de GMW is ingericht volgens de kwaliteitsnorm RWSgwmon.

    Document is in overtreding wanneer de GMW niet is ingericht volgens de kwaliteitsnorm RWSgwmon.
    """

    __feedbackMessage = "GMW is niet ingericht volgens de kwaliteitsnorm RWSgwmon."
    __explanation = "Regel die controleert of de GMW is ingericht volgens de kwaliteitsnorm RWSgwmon"
    code = 6
    name = "Kwaliteitsnorm"
    object_type = "GMW"

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

    def __validate_construction_standard(self, doc):
        construction_standard = doc.get_element_from_metadata("constructionStandard")
        return construction_standard == "RWSgwmon"

    def applyRule(self, doc):
        return (
            self.getFeedbackMessage()
            if (not self.__validate_construction_standard(doc))
            else None
        )
