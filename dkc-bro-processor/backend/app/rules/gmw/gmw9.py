from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW9(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW9 controleert de hoogtes van alle peilbuizen en of deze op realistische afstand zijn van het maaiveld.
        Om dit te controleren wordt gekeken naar de velden groundLevelPosition, tubeTopPosition.
        De buis mag niet hoger dan 1.5 boven het maaiveld liggen en niet lager dan 0.5 meter onder het maaiveld.

        Document is in overtreding wanneer niet alle peilbuizen zich op een plausibele hoogte bevinden.
        """,
        feedback_message="%s",
        explanation="""
        Deze regel controleert of de buishoogten te hoog (1,5m) of te laag (-0,5m) zijn gesitueerd ten opzichte van
        maaiveldpositie.
        """,
        code="09",
        name="Buishoogte ten opzichte van maaiveld",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def validate_tube_heights(payload: XmlParser) -> list:
        maaiveldpositie_elem = payload.get_element_by_tag_name("groundLevelPosition")
        offset_elem = payload.get_element_by_tag_name("offset")
        if maaiveldpositie_elem is None or offset_elem is None or maaiveldpositie_elem.text is None or offset_elem.text is None:
            return []

        maaiveldpositie = float(maaiveldpositie_elem.text)
        offset = float(offset_elem.text)
        tube_issues = []

        monitoring_tubes = payload.get_list_of_elements_by_tag_name("monitoringTube") or []
        for monitoring_tube in monitoring_tubes:
            tube_number = payload.get_child_element_by_tag_name(monitoring_tube, "tubeNumber")
            tube_top_position = payload.get_child_element_by_tag_name(monitoring_tube, "tubeTopPosition")
            if tube_number is None or tube_top_position is None or tube_number.text is None or tube_top_position.text is None:
                continue

            tube_id = int(tube_number.text)
            tube_top_position = float(tube_top_position.text)
            calc_value = tube_top_position - maaiveldpositie + offset
            if calc_value < -0.5:
                tube_issues.append((tube_id, "te laag", calc_value))
            elif calc_value > 1.5:
                tube_issues.append((tube_id, "te hoog", calc_value))
        return tube_issues

    @staticmethod
    def get_specific_message(payload: XmlParser, tube_issues: list) -> str:
        maaiveldpositie_elem = payload.get_element_by_tag_name("groundLevelPosition")
        if maaiveldpositie_elem is None or maaiveldpositie_elem.text is None:
            return ""

        maaiveldpositie = float(maaiveldpositie_elem.text)
        messages = []
        for tube_id, issue, value in tube_issues:
            if issue == "te hoog":
                messages.append(
                    f"Buishoogte van buis '{tube_id}' is te hoog ({value:.2f}m) gesitueerd ten opzichte \
                        van maaiveldpositie: '{maaiveldpositie}m'."
                )
            elif issue == "te laag":
                messages.append(
                    f"Buishoogte van buis '{tube_id}' is te laag ({value:.2f}m) gesitueerd ten opzichte \
                        van maaiveldpositie: '{maaiveldpositie}m'."
                )
        return "\n".join(messages)

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        tube_issues = self.validate_tube_heights(payload)
        if tube_issues:
            specific_message = self.get_specific_message(payload, tube_issues)
            feedback_message = self.rule_info.feedback_message % specific_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
