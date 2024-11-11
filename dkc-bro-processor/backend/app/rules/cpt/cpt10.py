from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT10(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT10 controleert of het Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) is ingevuld

        Document is in overtreding wanneer Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) niet is ingevuld.
        """,
        feedback_message="Sondeerapparaat Oppervlakte kleefmantel (frictionSleeveSurfaceArea) is niet ingevuld",
        explanation="Controleert of oppervlakte kleefmantel (frictionSleeveSurfaceArea) ingevuld is in het brondocument",
        code="010",
        name="Oppervlakte kleefmantel",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_friction_sleeve_surface_area(payload: CPTParser):
        return payload.get_element_from_metadata("frictionSleeveSurfaceArea")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        friction_sleeve_surface_area = self.check_friction_sleeve_surface_area(payload)
        if friction_sleeve_surface_area is None:
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
