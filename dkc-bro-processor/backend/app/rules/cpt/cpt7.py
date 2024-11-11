from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT7(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT7 controleert of het Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse4.
        Indien dit het geval is moet er bij een adviseur worden nagegaan of dit voor dit project wenselijk is.

        Document is in overtreding wanneer Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse4.
        """,
        feedback_message="""
        Domein Kwaliteitsklasse (qualityClass) is gevuld met waarde klasse4. Vraag een adviseur of deze waarde legitiem is
        voor dit project.
        """,
        explanation="""
        Controleert of het Domein Kwaliteitsklasse (qualityClass) gevuld met klasse4. Indien dit het geval is wordt er een
        melding gedaan met verzoek tot raadpleding van een adviseur.
        """,
        code="07",
        name="Domein Kwaliteitsklasse (BRO)",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_quality_class(payload: CPTParser):
        return payload.get_element_from_metadata("qualityClass")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        quality_class = self.check_quality_class(payload)
        if quality_class == "klasse4":
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
