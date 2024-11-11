# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0009(superRule):
    __docstring = """
    Controleregel GMW0009 controleert de hoogtes van alle peilbuizen en of deze op realistische afstand zijn van het maaiveld.
    Om dit te controleren wordt gekeken naar de velden groundLevelPosition, tubeTopPosition.
    De buis mag niet hoger dan 1.5 boven het maaiveld liggen en niet lager dan 0.5 meter onder het maaiveld.

    Document is in overtreding wanneer niet alle peilbuizen zich op een plausibele hoogte bevinden.
    """

    __feedbackMessage = "Buishoogte van een of meer buizen is te hoog (1,5m) of te laag (-0,5m) gesitueerd ten opzichte van maaiveldpositie."
    __explanation = "Deze regel controleert of de buishoogten te hoog (1,5m) of te laag (-0,5m) zijn gesitueerd ten opzichte van maaiveldpositie."
    code = 9
    name = "Buishoogte ten opzichte van maaiveld"
    object_type = "GMW"

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

    def __validate_tube_heights(self, doc):
        maaiveldpositie = float(doc.get_element_by_tag_name("groundLevelPosition").text)
        offset = float(doc.get_element_by_tag_name("offset").text)
        for monitoring_tube in doc.get_list_of_elements_by_tag_name("monitoringTube"):
            tube_top_position = float(
                doc.get_child_element_by_tag_name(
                    monitoring_tube, "tubeTopPosition"
                ).text
            )
            calc_value = tube_top_position - maaiveldpositie + offset
            if calc_value < -0.5 or calc_value > 1.5:
                return False
        return True

    def applyRule(self, doc):
        return (
            self.getFeedbackMessage()
            if (not self.__validate_tube_heights(doc))
            else None
        )
