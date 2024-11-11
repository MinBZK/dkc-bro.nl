# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BRO0002(superRule):
    __docstring = """
    Controleregel BRO0002 controleert of het kwaliteitsregime (qualityRegime) gelijk is aan IMBRO.
    qualityRegime wordt door middel van XML-parsing uit het brondocument gelezen en vergeleken met de waarde "IMBRO".

    Document is in overtreding wanneer de uitgelezen waarde niet gelijk is aan "IMBRO".
    """
    __feedbackMessage = "Kwaliteitsregime (qualityRegime) is niet gelijk aan IMBRO."
    __explanation = (
        "Controleert of het kwaliteitsregime (qualityRegime) gelijke is aan IMBRO."
    )
    code = 2
    name = "Kwaliteitsregime"
    object_type = "BRO"

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
            None
            if (doc.get_element_from_metadata("qualityRegime") == "IMBRO")
            else self.getFeedbackMessage()
        )
