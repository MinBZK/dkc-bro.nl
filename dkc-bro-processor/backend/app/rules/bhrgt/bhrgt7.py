from app.parsers.bhrgt_parser import BHRGTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class BHR_GT7(BaseRule[BHRGTParser]):
    supported_payload_types = [BHRGTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel BHR_GT7 controleert of de beschrijfprocedure (descriptionProcedure) van het document volgens ISO14688 is.

        Document is in overtreding wanneer beschrijfprocedure (descriptionProcedure) van het document niet de waarde '14688' bevat.
        """,
        feedback_message="""
        De beschrijfprocedure (descriptionProcedure) van het document bevat niet de waarde '14688'.
        De gevonden waarde is '%s'
        """,
        explanation="Controleert of de beschrijfprocedure (descriptionProcedure) van het document de waarde '14688' bevat.",
        code="07",
        name="Beschrijfprocedure",
        object_type=ObjectType.BHR_GT,
    )

    valid_procedure: str = "14688"

    @staticmethod
    def check_description_procedure(payload: BHRGTParser):
        return payload.get_element_from_metadata("descriptionProcedure")

    def apply_rule(self, payload: BHRGTParser) -> RuleResult:
        description_procedure = self.check_description_procedure(payload)

        if description_procedure and self.valid_procedure not in description_procedure:
            feedback_message = self.rule_info.feedback_message % description_procedure
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
