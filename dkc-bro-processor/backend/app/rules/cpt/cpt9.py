from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT9(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT9 controleert of het Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) is ingevuld

        Document is in overtreding wanneer Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) niet is ingevuld.
        """,
        feedback_message="Sondeerapparaat Oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) is niet ingevuld",
        explanation="Controleert of oppervlaktequotient kleefmantel (frictionSleeveSurfaceQuotient) ingevuld is in het brondocument",
        code="09",
        name="Oppervlaktequotient kleefmantel",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_friction_sleeve_surface_quotient(payload: CPTParser):
        return payload.get_element_from_metadata("frictionSleeveSurfaceQuotient")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        friction_sleeve_surface_quotient = self.check_friction_sleeve_surface_quotient(payload)
        if friction_sleeve_surface_quotient is None:
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
