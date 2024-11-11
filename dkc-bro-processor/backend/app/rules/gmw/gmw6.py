from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW6(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW6 controleert of de GMW is ingericht volgens de kwaliteitsnorm RWSgwmon.

        Document is in overtreding wanneer de GMW niet is ingericht volgens de kwaliteitsnorm RWSgwmon.
        """,
        feedback_message="GMW is niet ingericht volgens de kwaliteitsnorm RWSgwmon. De gevonden waarde is: '%s'.",
        explanation="Regel die controleert of de GMW is ingericht volgens de kwaliteitsnorm RWSgwmon",
        code="06",
        name="Kwaliteitsnorm",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def check_construction_standard(payload: XmlParser):
        construction_standard = payload.get_element_from_metadata("constructionStandard")

        if construction_standard != "RWSgwmon":
            return construction_standard
        return ""

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        invalid_standard = self.check_construction_standard(payload)

        if invalid_standard:
            feedback_message = self.rule_info.feedback_message % invalid_standard
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
