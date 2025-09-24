# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GEN0003(superRule):
    __docstring = """
    Controleregel GEN0003 controleert of de Domein Kader Aanlevering (deliveryContext) gelijk is aan publieke taak uitvoering (publiekeTaak) of rechtsgrond waterwet (WW).

    Document is in overtreding wanneer Domein Kader Aanlevering (deliveryContext) niet gelijk is aan publieke taak uitvoering (publiekeTaak) of rechtsgrond waterwet (WW).
    """

    __feedbackMessage = "Domein Kader Aanlevering (deliveryContext) is ongeldig ingevuld. De gevonden waarde is: '%s'."
    __explanation = "Controleert of het Domein Kader Aanlevering (deliveryContext) gelijk is aan publieke taak uitvoering (publiekeTaak) of rechtsgrond waterwet (WW)."
    code = "03"
    name = "Domein Kader Aanlevering"
    object_type = "GEN"
    valid_delivery_contexts = ["publiekeTaak", "WW"]

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
        valid_context = doc.get_element_from_metadata("deliveryContext")
        if valid_context not in self.valid_delivery_contexts:
            return self.getFeedbackMessage() % valid_context
        else:
            return None
