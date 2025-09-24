# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GEN0002(superRule):
    __docstring = """
    Controleregel GEN0002 controleert of het kwaliteitsregime (qualityRegime) gelijk is aan IMBRO.
    qualityRegime wordt door middel van XML-parsing uit het brondocument gelezen en vergeleken met de waarde "IMBRO".

    Document is in overtreding wanneer de uitgelezen waarde niet gelijk is aan "IMBRO".
    """
    __feedbackMessage = "Kwaliteitsregime (qualityRegime) is niet gelijk aan IMBRO. De gevonden waarde is: '%s'."
    __explanation = (
        "Controleert of het kwaliteitsregime (qualityRegime) gelijke is aan IMBRO."
    )
    code = "02"
    name = "Kwaliteitsregime"
    object_type = "GEN"

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
        quality_regime = doc.get_element_from_metadata("qualityRegime")
        if quality_regime != "IMBRO":
            return self.getFeedbackMessage() % quality_regime
        else:
            return None
