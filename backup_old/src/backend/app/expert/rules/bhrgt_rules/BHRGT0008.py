# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BHRGT0008(superRule):
    __docstring = """
    Controleregel BHRGT0008 controleert of de monstervochtigheid (sampleMoistness) is ingevuld voor een object.

    Document is in overtreding wanneer monstervochtigheid (sampleMoistness) niet is ingevuld of gelijk is aan onbekend.
    """

    __feedbackMessage = "Monstervochtigheid (sampleMoistness) is niet bekend."
    __explanation = "Controleert of de waarde voor Monstervochtigheid (sampleMoistness) niet onbekend is."
    code = 8
    name = "Monstervochtigheid"
    object_type = "BHR-GT"

    def __init__(self, emergence=enums.Importance.WARNING):
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
        sample_moistness = doc.get_element_from_metadata("sampleMoistness")
        return (
            self.getFeedbackMessage()
            if (not sample_moistness or sample_moistness == "onbekend")
            else None
        )
