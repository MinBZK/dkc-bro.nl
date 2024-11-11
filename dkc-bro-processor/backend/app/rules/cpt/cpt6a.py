from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT6A(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT6A controleert of het Domein Sondeernorm (cptStandard) niet is ingevuld met een van de ongeldige opties: NEN5140,
        NEN3680 of onbekend. Indien dit het geval is moet het bestand worden afgekeurd.

        Document is in overtreding wanneer Domein Sondeernorm (cptStandard) is ingevuld met een van de ongeldige opties: NEN5140, NEN3680
        of onbekend.
        """,
        feedback_message="Domein Sondeernorm (cptStandard) is ingevuld met een ongeldige optie: '%s'.",
        explanation="""
        Controleert of het Domein Sondeernorm (cptStandard) is ingevuld NEN5140, NEN3680 of onbekend. Wanneer dit het geval is
        dient het bestand te worden gerouterneerd.
        """,
        code="06A",
        name="Domein Sondeernorm (BRO) NEN5140, NEN3680 of onbekend.",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cpt_standard(payload: CPTParser):
        return payload.get_element_from_metadata("cptStandard")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        cpt_standard = self.check_cpt_standard(payload)
        if cpt_standard in ["NEN5140", "NEN3680", "onbekend"]:
            feedback_message = self.rule_info.feedback_message % cpt_standard
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
