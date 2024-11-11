from app.parsers.bhrgt_parser import BHRGTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class BHR_GT2(BaseRule[BHRGTParser]):
    supported_payload_types = [BHRGTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel BHR_GT2 controleert of het document een rapportagedatum (researchReportDate) bevat.

        Document is in overtreding wanneer researchReportDate niet bestaat of niet gevuld is.
        """,
        feedback_message="%s",
        explanation="Controleert of het brondocument een rapportagedatum (researchReportDate) bevat.",
        code="02",
        name="Rapportagedatum",
        object_type=ObjectType.BHR_GT,
    )

    @staticmethod
    def check_research_report_date(payload: BHRGTParser):
        return payload.get_element_from_metadata("researchReportDate")

    def apply_rule(self, payload: BHRGTParser) -> RuleResult:
        research_report_date = self.check_research_report_date(payload)
        if not research_report_date:
            specific_feedback_message = "Document bevat geen rapportagedatum (researchReportDate)."
            feedback_message = self.rule_info.feedback_message % specific_feedback_message
            passed = False
        elif not research_report_date.get("date"):
            specific_feedback_message = "Document bevat een rapportagedatum (researchReportDate) maar die is niet ingevuld."
            feedback_message = self.rule_info.feedback_message % specific_feedback_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
