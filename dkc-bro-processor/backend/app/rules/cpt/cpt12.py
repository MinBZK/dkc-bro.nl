from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT12(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT12 controleert of het Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) is ingevuld

        Document is in overtreding wanneer Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) niet is ingevuld.
        """,
        feedback_message="Sondeerapparaat Oppervlaktequotient conuspunt (coneSurfaceQuotient) is niet ingevuld",
        explanation="Controleert of element conuspunt (coneSurfaceQuotient) ingevuld is in het brondocument",
        code="012",
        name="Oppervlaktequotient conuspunt",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cone_surface_quotient(payload: CPTParser):
        return payload.get_element_from_metadata("coneSurfaceQuotient")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        cone_surface_quotient = self.check_cone_surface_quotient(payload)
        if cone_surface_quotient is None:
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
