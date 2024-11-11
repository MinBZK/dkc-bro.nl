from app.parsers.bhrgt_parser import BHRGTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class BHR_GT8(BaseRule[BHRGTParser]):
    supported_payload_types = [BHRGTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel BHR_GT8 controleert of de monstervochtigheid (sampleMoistness) is ingevuld voor een object.

        Document is in overtreding wanneer monstervochtigheid (sampleMoistness) niet is ingevuld of gelijk is aan onbekend.
        """,
        feedback_message="%s",
        explanation="Controleert of de waarde voor Monstervochtigheid (sampleMoistness) niet onbekend is.",
        code="08",
        name="Monstervochtigheid",
        object_type=ObjectType.BHR_GT,
    )

    @staticmethod
    def check_sample_moistness(payload: BHRGTParser):
        return payload.get_element_from_metadata("sampleMoistness")

    def apply_rule(self, payload: BHRGTParser) -> RuleResult:
        sample_moistness = self.check_sample_moistness(payload)

        if sample_moistness is None:
            specific_feedback_message = "Het veld Monstervochtigheid (sampleMoistness) is leeg."
            feedback_message = self.rule_info.feedback_message % specific_feedback_message
            passed = False
        elif not sample_moistness.strip():
            specific_feedback_message = "Monstervochtigheid (sampleMoistness) is ongeldig ingevuld."
            feedback_message = self.rule_info.feedback_message % specific_feedback_message
            passed = False
        elif sample_moistness == "onbekend":
            specific_feedback_message = "Monstervochtheid (sampleMoistness) is gelijk aan 'onbekend'."
            feedback_message = self.rule_info.feedback_message % specific_feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
