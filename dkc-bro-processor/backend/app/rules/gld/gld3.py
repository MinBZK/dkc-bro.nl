from datetime import datetime

from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GLD3(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GLD3 controleert of alle aangeboden metingen in het verleden liggen.
        Om dit te controleren worden de velden phenomenonTime => TimePeriod => endPosition gebruikt.

        Document is in overtreding wanneer een of meer aangeboden metingen in de toekomst liggen.
        """,
        feedback_message="Aangeboden meting(en) met ID: '%s' liggen in de toekomst. Vandaag is '%s'.",
        explanation="Controleert of alle aangeboden metingen in het verleden liggen.",
        code="03",
        name="Observatieperiode",
        object_type=ObjectType.GLD,
    )

    @staticmethod
    def check_phenomenon_times(payload: XmlParser) -> list:
        now = datetime.now()
        phenomenon_times = payload.get_list_of_elements_by_tag_name("phenomenonTime") or []
        future_dates = []

        for i, pt in enumerate(phenomenon_times):
            time_period = payload.get_child_element_by_tag_name(pt, "TimePeriod")
            if time_period is None:
                continue
            end_date = payload.get_child_element_by_tag_name(time_period, "endPosition")
            if end_date is None or end_date.text is None:
                continue
            try:
                end_date_datetime = datetime.fromisoformat(end_date.text)
                if end_date_datetime > now:
                    future_dates.append(str(i + 1))
            except ValueError:
                # Handle invalid date format
                continue

        return future_dates

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        future_dates = self.check_phenomenon_times(payload)

        if future_dates:
            now = datetime.now()
            future_dates_str = ", ".join(future_dates)
            feedback_message = self.rule_info.feedback_message % (
                future_dates_str,
                now.strftime("%d-%m-%Y %H:%M"),
            )
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
