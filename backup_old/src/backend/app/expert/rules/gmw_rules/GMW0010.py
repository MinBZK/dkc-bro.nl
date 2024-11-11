# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0010(superRule):
    __docstring = """
    Controleregel GMW0010 controleert of de bovenkanten van peilbuizen binnen een GMW niet te veel verschillen in hoogte, oplopend van de diepste filter tot de ondiepste filter.
    Per peilbuis worden door middel van XML-parsing de volgende eigenschappen uitgelezen uit het brondocument: "tubeNumber, tubeTopPosition, plainTubePartLength, screenLength".
    De ingelezen peilbuizen worden gesorteerd op basis van diep naar ondiep.
    Om dit te kunnen doen worden de onderposities per buis berekend uit de velden tubeTopPosition, plainTubePartLength, screenLength.
    Onderpositie = tubeTopPosition - plainTubePartLength + screenLength.
    Vervolgens wordt gekeken of tussen de gesorteerde buizen er steeds een maximaal verschil van 0.02m in hoogte (tubeTopPosition) is.

    Document is in overtreding wanneer voor minstens één opvolgend paar peilbuizen het hoogteverschil groter is dan 0.02m.
    """

    __feedbackMessage = "De bovenkanten van de peilbuizen verschillen niet in hoogte, oplopend van diepste filter tot hoogste filter."
    __explanation = """Bij meerdere peilbuizen in een put moeten de de bovenkanten van de peilbuizen minimaal 0.02m in hoogte verschillen, 
                       waarbij de hoogte oploopt van de buis met het diepste filter tot de buis met de hoogste filter."""
    code = 10
    name = "Hoogte bovenkant peilbuizen"
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

    def __calculate_bottom_position(self, doc, monitoring_tube):
        return float(
            doc.get_child_element_by_tag_name(monitoring_tube, "tubeTopPosition").text
        ) - (
            float(
                doc.get_child_element_by_tag_name(
                    monitoring_tube, "plainTubePartLength"
                ).text
            )
            + float(
                doc.get_child_element_by_tag_name(monitoring_tube, "screenLength").text
            )
        )

    def __validate_tube_differences(self, doc):
        tubes = [
            {
                "number": float(
                    doc.get_child_element_by_tag_name(
                        monitoring_tube, "tubeNumber"
                    ).text
                ),
                "top_position": float(
                    doc.get_child_element_by_tag_name(
                        monitoring_tube, "tubeTopPosition"
                    ).text
                ),
                "bottom_position": self.__calculate_bottom_position(
                    doc, monitoring_tube
                ),
            }
            for monitoring_tube in doc.get_list_of_elements_by_tag_name(
                "monitoringTube"
            )
        ]
        if len(tubes) == 1:
            return True
        else:
            sorted_tubes = sorted(
                tubes, key=lambda tube: tube.get("bottom_position"), reverse=False
            )
            for i in range(0, len(sorted_tubes) - 1):
                if (
                    sorted_tubes[i].get("top_position")
                    - sorted_tubes[i + 1].get("top_position")
                    > -0.02
                ):
                    return False
            return True

    def applyRule(self, doc):
        return (
            self.getFeedbackMessage()
            if (not self.__validate_tube_differences(doc))
            else None
        )
