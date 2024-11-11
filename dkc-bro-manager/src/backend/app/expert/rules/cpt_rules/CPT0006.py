# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0006(superRule):
    __docstring = """
    Controleregel CPT0006 controleert of het Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12.
    Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

    Document is in overtreding wanneer Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12.
    """
    __feedbackMessage = "Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12. Ga na bij een specialist/adviseur of dit legitiem is voor het project."
    __explanation = "Controleert of het Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12. Wanneer dit het geval is dient er een vraag doorgezet te worden naar een specialist."
    code = "06"
    name = "Domein Sondeernorm (BRO) NEN-EN-ISO 22476 deel 12."
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
            if (doc.get_element_from_metadata("cptStandard") == "ISO22476D12")
            else None
        )
