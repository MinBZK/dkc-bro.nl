# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0007A(superRule):
    __docstring = """
    Controleregel CPT0007A controleert of het Domein Kwaliteitsklasse (qualityClass) is gevuld met een geldige waarde.
    De regel bevat een lijst van niet-geldige waarden waar tegen de waarde uit het document wordt vergeleken.
    De lijst bevat de waardes klasse 4 en alles lager dan klasse 4.

    Document is in overtreding wanneer Domein Kwaliteitsklasse (qualityClass) is gevuld met een waarde uit de lijst niet geldige kwaliteitsklassen.
    """

    __feedbackMessage = (
        "Domein Kwaliteitsklasse (qualityClass) is gevuld met een niet geldige waarde."
    )
    __explanation = "Controleert of het Domein Kwaliteitsklasse (qualityClass) gevuld is met klasse4 of lager. Indien dit het geval is moet het object gerouterneerd worden."
    code = "7A"
    name = "Domein Kwaliteitsklasse (BRO)"
    object_type = "CPT"
    invalid_quality_classes = [
        "klasse4",
        "klasse5",
        "klasse6",
        "klasse7",
        "nvt",
        "onbekend",
    ]

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
            if (
                doc.get_element_from_metadata("qualityClass")
                in self.invalid_quality_classes
            )
            else None
        )
