from datetime import datetime, timedelta

from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GLD4(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GLD4 controleert of alle aangeboden metingen in de laatste 20 dagen zijn aangeboden.
        Om dit te controleren worden de velden resultTime => TimeInstant => timePosition gebruikt.

        Document is in overtreding wanneer een of meer aangeboden metingen niet in de laatste 20 dagen zijn aangeboden.
        """,
        feedback_message="Meting(en): '%s' zijn meer dan 20 dagen geleden ingewonnen: '%s'.",
        explanation="Controleert of alle aangeboden metingen niet eerder dan 20 dagen geleden zijn ingewonnen.",
        code="04",
        name="Tijdstip resultaat",
        object_type=ObjectType.GLD,
    )

    @staticmethod
    def check_result_times(payload: XmlParser) -> list:
        now = datetime.now().replace(tzinfo=None)  # Added check to remove timezone info - essentially making it Naive
        result_times = payload.get_list_of_elements_by_tag_name("resultTime") or []
        faulty_result_times = []

        for index, rt in enumerate(result_times, start=1):
            time_instant = payload.get_child_element_by_tag_name(rt, "TimeInstant")
            if time_instant is None:
                continue
            time_position = payload.get_child_element_by_tag_name(time_instant, "timePosition")
            if time_position is None or time_position.text is None:
                continue
            try:
                result_time = datetime.fromisoformat(time_position.text).replace(tzinfo=None)
                if result_time < (now - timedelta(days=20)):
                    faulty_result_times.append((index, time_position.text))
            except ValueError:
                # Handle invalid date format
                continue

        return faulty_result_times

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        faulty_result_times = self.check_result_times(payload)

        if faulty_result_times:
            indices, values = zip(*faulty_result_times)
            feedback_message = self.rule_info.feedback_message % (
                ", ".join(map(str, indices)),
                ", ".join(values),
            )
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
