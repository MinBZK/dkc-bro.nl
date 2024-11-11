from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GEN3(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GEN3 controleert of de Domein Kader Aanlevering (deliveryContext) gelijk is aan publieke taak uitvoering
        (publiekeTaak) of rechtsgrond waterwet (WW).

        Document is in overtreding wanneer Domein Kader Aanlevering (deliveryContext) niet gelijk is aan publieke taak uitvoering
        (publiekeTaak) of rechtsgrond waterwet (WW).
        """,
        feedback_message="Domein Kader Aanlevering (deliveryContext) is ongeldig ingevuld. De gevonden waarde is: '%s'.",
        explanation="""
        Controleert of het Domein Kader Aanlevering (deliveryContext) gelijk is aan publieke taak uitvoering (publiekeTaak)
        of rechtsgrond waterwet (WW).
        """,
        code="03",
        name="Domein Kader Aanlevering",
        object_type=ObjectType.GEN,
    )

    valid_delivery_contexts = ["publiekeTaak", "WW"]

    @classmethod
    def check_delivery_context(cls, delivery_context: str) -> bool:
        return delivery_context in cls.valid_delivery_contexts

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        delivery_context = payload.get_element_from_metadata("deliveryContext")

        if not delivery_context or not self.check_delivery_context(delivery_context):
            feedback_message = self.rule_info.feedback_message % delivery_context
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
