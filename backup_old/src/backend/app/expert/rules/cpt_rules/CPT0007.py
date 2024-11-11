# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0007(superRule):
    __docstring = """
    Controleregel CPT0007 controleert of het Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse3.
    Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

    Document is in overtreding wanneer Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse3.
    """

    __feedbackMessage = "Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse3. Vraag een adviseur of deze waarde legitiem is voor dit project."
    __explanation = "Controleert of het Domein Kwaliteitsklasse (qualityClass) gevuld met klasse3. Indien dit het geval is wordt er een melding gedaan met verzoek tot raadpleding van een adviseur."
    code = "7"
    name = "Domein Kwaliteitsklasse (BRO)"
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
            if (doc.get_element_from_metadata("qualityClass") == "klasse3")
            else None
        )
