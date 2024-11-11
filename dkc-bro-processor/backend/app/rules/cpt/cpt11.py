from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT11(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT11 controleert of het Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance)
        is ingevuld

        Document is in overtreding wanneer Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance)
        niet is ingevuld.
        """,
        feedback_message="Sondeerapparaat afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) is niet ingevuld",
        explanation="Controleert of afstand conus tot midden kleefmantel (coneToFrictionSleeveDistance) aanwezig is in het brondocument",
        code="011",
        name="Afstand conus tot midden kleefmantel",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cone_to_friction_sleeve_distance(payload: CPTParser):
        return payload.get_element_from_metadata("coneToFrictionSleeveDistance")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        cone_to_friction_sleeve_distance = self.check_cone_to_friction_sleeve_distance(payload)
        if cone_to_friction_sleeve_distance is None:
            feedback_message = self.rule_info.feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
