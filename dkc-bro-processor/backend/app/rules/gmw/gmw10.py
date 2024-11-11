from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW10(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW0010 controleert of de bovenkanten van peilbuizen binnen een GMW niet te veel verschillen in hoogte, oplopend van
        de diepste filter tot de ondiepste filter.
        Per peilbuis worden door middel van XML-parsing de volgende eigenschappen uitgelezen uit het brondocument: "tubeNumber,
        tubeTopPosition, mplainTubePartLength, screenLength".
        De ingelezen peilbuizen worden gesorteerd op basis van diep naar ondiep.
        Om dit te kunnen doen worden de onderposities per buis berekend uit de velden tubeTopPosition, plainTubePartLength, screenLength.
        Onderpositie = tubeTopPosition - plainTubePartLength + screenLength.
        Vervolgens wordt gekeken of tussen de gesorteerde buizen er steeds een maximaal verschil van 0.02m in hoogte (tubeTopPosition) is.

        Document is in overtreding wanneer voor minstens één opvolgend paar peilbuizen het hoogteverschil groter is dan 0.02m.
        """,
        feedback_message="%s",
        explanation="""Bij meerdere peilbuizen in een put moeten de de bovenkanten van de peilbuizen minimaal 0.02m in hoogte verschillen,
                       waarbij de hoogte oploopt van de buis met het diepste filter tot de buis met de hoogste filter.""",
        code="010",
        name="Hoogte bovenkant peilbuizen",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def get_tube_data(payload: XmlParser) -> list:
        tubes = []
        monitoring_tubes = payload.get_list_of_elements_by_tag_name("monitoringTube") or []
        for monitoring_tube in monitoring_tubes:
            tube_number = payload.get_child_element_by_tag_name(monitoring_tube, "tubeNumber")
            tube_top_position = payload.get_child_element_by_tag_name(monitoring_tube, "tubeTopPosition")
            plain_tube_part_length = payload.get_child_element_by_tag_name(monitoring_tube, "plainTubePartLength")
            screen_length = payload.get_child_element_by_tag_name(monitoring_tube, "screenLength")

            if all(
                elem is not None and elem.text is not None
                for elem in [
                    tube_number,
                    tube_top_position,
                    plain_tube_part_length,
                    screen_length,
                ]
            ):
                tubes.append(
                    {
                        "number": float(tube_number.text) if tube_number is not None else None,
                        "top_position": float(tube_top_position.text) if tube_top_position is not None else None,
                        "bottom_position": (
                            float(tube_top_position.text)
                            - (
                                float(plain_tube_part_length.text)
                                if plain_tube_part_length is not None
                                else 0 + float(screen_length.text) if screen_length is not None else 0
                            )
                            if tube_top_position is not None
                            else None
                        ),
                    }
                )
        return tubes

    @staticmethod
    def check_tube_heights(tubes: list) -> list:
        tubes.sort(key=lambda x: x["bottom_position"], reverse=True)
        violations = []

        for i in range(len(tubes) - 1):
            height_difference = abs(tubes[i]["top_position"] - tubes[i + 1]["top_position"])
            if height_difference > 0.02:
                violations.append((tubes[i]["number"], tubes[i + 1]["number"], height_difference))

        return violations

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        tubes = self.get_tube_data(payload)
        violations = self.check_tube_heights(tubes)

        if violations:
            violation_details = ", ".join(
                [
                    f"De bovenkanten van peilbuizen met ID: '{v[0]} en {v[1]}' hebben een hoogteverschil groter dan 0.02m.\
                    De gevonden waarde is: {v[2]:.3f}m."
                    for v in violations
                ]
            )
            feedback_message = self.rule_info.feedback_message % violation_details
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
