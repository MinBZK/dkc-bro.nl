# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0006A(superRule):
    __docstring = """
    Controleregel CPT0006A controleert of het Domein Sondeernorm (cptStandard) niet is ingevuld met een van de ongeldige opties: NEN5140, NEN3680 of onbekend.
    Indien dit het geval is moet het bestand worden afgekeurd.

    Document is in overtreding wanneer Domein Sondeernorm (cptStandard) is ingevuld met een van de ongeldige opties: NEN5140, NEN3680 of onbekend."
    """

    __feedbackMessage = "Domein Sondeernorm (cptStandard) is ingevuld met een van de ongeldige opties: NEN5140, NEN3680 of onbekend."
    __explanation = "Controleert of het Domein Sondeernorm (cptStandard) is ingevuld NEN5140, NEN3680 of onbekend. Wanneer dit het geval is dient het bestand te worden gerouterneerd.."
    code = "6A"
    name = "Domein Sondeernorm (BRO) NEN5140, NEN3680 of onbekend."
    object_type = "CPT"

    def __init__(self, emergence=enums.Importance.ERROR):
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
            if (
                doc.get_element_from_metadata("cptStandard")
                in ["NEN5140", "NEN3680", "onbekend"]
            )
            else None
        )
