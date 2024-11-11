from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT13(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT13 controleert of het Sondeerapparaat Conusdiameter (coneDiameter) is ingevuld

        Document is in overtreding wanneer Sondeerapparaat Conusdiameter (coneDiameter) niet is ingevuld.
        """,
        feedback_message="Sondeerapparaat Conusdiameter (coneDiameter) is niet ingevuld",
        explanation="Controleert of conusdiameter (coneDiameter) ingevuld is in het brondocument",
        code="013",
        name="Conusdiameter",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cone_diameter(payload: CPTParser):
        return payload.get_element_from_metadata("coneDiameter")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        cone_diameter = self.check_cone_diameter(payload)
        if cone_diameter is None:
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
