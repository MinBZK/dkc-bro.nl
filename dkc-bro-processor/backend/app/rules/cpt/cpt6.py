from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT6(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT6 controleert of het Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12.
        Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

        Document is in overtreding wanneer Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12.
        """,
        feedback_message="""
        Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12. Ga na bij een specialist/adviseur of
        dit legitiem is voor het project.
        """,
        explanation="""
        Controleert of het Domein Sondeernorm (cptStandard) is ingevuld met NEN-EN-ISO 22476 deel 12. Wanneer dit het geval is
        dient er een vraag doorgezet te worden naar een specialist.
        """,
        code="06",
        name="Domein Sondeernorm (BRO) NEN-EN-ISO 22476 deel 12.",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cpt_standard(payload: CPTParser) -> bool:
        return payload.get_element_from_metadata("cptStandard") == "ISO22476D12"

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        if self.check_cpt_standard(payload):
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
