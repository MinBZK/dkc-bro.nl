# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BHRGT0008(superRule):
    __docstring = """
    Controleregel BHRGT0008 controleert of de monstervochtigheid (sampleMoistness) is ingevuld voor een object.

    Document is in overtreding wanneer monstervochtigheid (sampleMoistness) niet is ingevuld of gelijk is aan onbekend.
    """

    __feedbackMessage = "%s"
    __explanation = "Controleert of de waarde voor Monstervochtigheid (sampleMoistness) niet onbekend is."
    code = "08"
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
        if sample_moistness is None:
            specific_feedbackmessage = (
                "Het veld Monstervochtigheid (sampleMoistness) is leeg."
            )
            return self.getFeedbackMessage() % specific_feedbackmessage
        elif not sample_moistness.strip():
            specific_feedbackmessage = (
                "Monstervochtigheid (sampleMoistness) is ongeldig ingevuld."
            )
            return self.getFeedbackMessage() % specific_feedbackmessage

        elif sample_moistness == "onbekend":
            specific_feedbackmessage = (
                "Monstervochtheid (sampleMoistness) is gelijk aan: 'onbekend'."
            )
            return self.getFeedbackMessage() % specific_feedbackmessage
        else:
            return None
