from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT8(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT8 controleert of het Domein Sondeermethode (cptMethod) is ingevuld met mechanischContinu of mechanischDiscontinu.
        Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

        Document is in overtreding wanneer Domein Sondeermethode (cptMethod) is ingevuld met mechanischContinu of mechanischDiscontinu.
        """,
        feedback_message="""
        Domein Sondeermethode (cptMethod) is ingevuld met: '%s'. Vraag na bij een adviseur of dit geschikt is
        voor dit project.
        """,
        explanation="""
        Controleert of het Domein Sondeermethode (cptMethod) gevuld is met mechanischContinu of mechanischDiscontinu.
        Als dit zo is moet er navraag gedaan worden bij een adviseur.
        """,
        code="08",
        name="Domein Sondeermethode (BRO) mechanischContinu of mechanischDiscontinu",
        object_type=ObjectType.CPT,
    )

    invalid_cpt_methods = ["mechanischContinu", "mechanischDiscontinu"]

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
