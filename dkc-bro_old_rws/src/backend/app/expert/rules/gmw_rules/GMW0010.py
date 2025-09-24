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

    __feedbackMessage = "%s"
    __explanation = """Bij meerdere peilbuizen in een put moeten de de bovenkanten van de peilbuizen minimaal 0.02m in hoogte verschillen, 
                       waarbij de hoogte oploopt van de buis met het diepste filter tot de buis met de hoogste filter."""
    code = "010"
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

    def applyRule(self, doc):
        # Gather all data: tube numbers, top positions, bottom positions and calculate differences
        tubes = [
            {
                "number": float(
                    doc.get_child_element_by_tag_name(
                        monitoring_tubes, "tubeNumber"
                    ).text
                ),
                "top_position": float(
                    doc.get_child_element_by_tag_name(
                        monitoring_tubes, "tubeTopPosition"
                    ).text
                ),
                "bottom_position": float(
                    doc.get_child_element_by_tag_name(
                        monitoring_tubes, "tubeTopPosition"
                    ).text
                )
                - (
                    float(
                        doc.get_child_element_by_tag_name(
                            monitoring_tubes, "plainTubePartLength"
                        ).text
                    )
                    + float(
                        doc.get_child_element_by_tag_name(
                            monitoring_tubes, "screenLength"
                        ).text
                    )
                ),
            }
            for monitoring_tubes in doc.get_list_of_elements_by_tag_name(
                "monitoringTube"
            )
        ]

        tubes.sort(key=lambda x: x["bottom_position"], reverse=True)

        violations = []

        for i in range(len(tubes) - 1):
            height_difference = abs(
                tubes[i]["top_position"] - tubes[i + 1]["top_position"]
            )
            if height_difference > 0.02:
                violations.append(
                    (tubes[i]["number"], tubes[i + 1]["number"], height_difference)
                )

        if violations:
            violation_details = ", ".join(
                [
                    f"De bovenkanten van peilbuizen met ID: '{v[0]} en {v[1]}' hebben een hoogteverschil groter dan 0.02m. De gevonden waarde is: {v[2]:.2f}m."
                    for v in violations
                ]
            )
            return self.getFeedbackMessage() % violation_details
        else:
            return None
