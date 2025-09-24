# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule
from app.utils.parser_utils import XLINKHREF


class GLD0008(superRule):
    __docstring = """
    Controleregel GLD0008 controleert of de status van kwaliteitscontrole voor alle aangeboden metingen of goedgekeurd is of nog niet beoordeeld.
    Om dit te controleren worden de velden TVPMeasurementMetadata, qualifier, Category, codeSpace, value gebruikt.

    Document is in overtreding wanneer de status van kwaliteitscontrole niet voor alle metingen goedgekeurd is of nog niet beoordeeld.
    """

    __feedbackMessage = "De status van kwaliteitscontrole van een of meerdere metingen is niet gelijk aan goedgekeurd of nog niet beoordeeld. Gevonden waarden: '%s'."
    __explanation = "Controleert of de status van kwaliteitscontrole gelijk is aan goedgekeurd of nog niet beoordeeld voor alle aangeleverde metingen."
    code = "08"
    name = "Statuskwaliteitscontrole"
    object_type = "GLD"

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
        faulty_statusses = []
        measurements = doc.get_list_of_elements_by_tag_name("TVPMeasurementMetadata")
        if measurements:
            for m in measurements:
                qualifier = doc.get_child_element_by_tag_name(m, "qualifier")
                for c in doc.get_child_elements_by_tag_name(qualifier, "Category"):
                    codespace = doc.get_child_element_by_tag_name(c, "codeSpace")
                    value = doc.get_child_element_by_tag_name(c, "value")
                    if (
                        codespace.attrib[XLINKHREF]
                        == "urn:bro:gld:StatusQualityControl"
                    ):
                        if value.text not in ["goedgekeurd", "nogNietBeoordeeld"]:
                            faulty_statusses.append(value.text)
        return (
            self.getFeedbackMessage() % (",".join(list(set(faulty_statusses))))
            if len(faulty_statusses) > 0
            else None
        )
