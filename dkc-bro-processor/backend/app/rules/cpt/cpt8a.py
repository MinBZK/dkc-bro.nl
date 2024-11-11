from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT8A(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT8A controleert of het Domein Sondeermethode (cptMethod) is ingevuld met elektrisch, mechanisch of onbekend.

        Document is in overtreding wanneer Domein Sondeermethode (cptMethod) is ingevuld met elektrisch, mechanisch of onbekend.
        """,
        feedback_message="Domein Sondeermethode (cptMethod) is ingevuld met een niet geldige waarde: '%s'.",
        explanation="""
        Controleert of het Domein Sondeermethode (cptMethod) gevuld is met elektrisch, mechanisch of onbekend. Als dit zo is moet er
        gerouterneerd worden.
        """,
        code="08A",
        name="Domein Sondeermethode (BRO) elektrisch, mechanisch of onbekend",
        object_type=ObjectType.CPT,
    )

    invalid_cpt_methods = [
        "elektrisch",
        "mechanisch",
        "onbekend",
    ]

    @staticmethod
    def check_cpt_method(payload: CPTParser):
        return payload.get_element_from_metadata("cptMethod")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        cpt_method = self.check_cpt_method(payload)
        if cpt_method in self.invalid_cpt_methods:
            feedback_message = self.rule_info.feedback_message % cpt_method
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
