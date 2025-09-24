# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class CPT0005(superRule):
    __docstring = """
    Controleregel CPT0005 controleert of het domein Stopcriterium correct is ingevuld. De regel bevat een lijst van valide stop criteria en
    legt het veld Domein Stopcriterium (stopCriterion) hier tegen aan.

    Document is in overtreding wanneer Domein Stopcriterium (stopCriterion) niet aanwezig is in de lijst van valide stopcriteria.
    """
    __feedbackMessage = "%s"
    __explanation = "Controleert of het Domein Stopcriterium (stopCriterion) gevuld is met een geldige waarde uit de codelijst die niet gelijk is aan onbekend."
    code = "05"
    name = "Domein Stopcriterium (BRO)"
    object_type = "CPT"
    valid_stop_criterions = [
        "bezwijkrisico",
        "conusweerstand",
        "einddiepte",
        "hellingshoek",
        "obstakel",
        "storing",
        "waterspanning",
        "wegdrukkracht",
        "wrijvingsweerstand",
    ]

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
        stop_criterion = doc.get_element_from_metadata("stopCriterion")

        if stop_criterion == "onbekend":
            specific_message = f"Domein Stopcriterium (stopCriterion) is met een waarde ingevuld met de waarde: '{stop_criterion}'."
            return self.getFeedbackMessage() % specific_message

        elif stop_criterion not in self.valid_stop_criterions:
            specific_message = f"Domein Stopcriterium (stopCriterion) is ingevuld met een waarde die niet op de codelijst staat: '{stop_criterion}'."
            return self.getFeedbackMessage() % specific_message

        elif stop_criterion in self.valid_stop_criterions:
            return None
