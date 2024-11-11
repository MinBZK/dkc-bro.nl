# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BHRGT0002(superRule):
    __docstring = """
    Controleregel BHRGT0002 controleert of het document een rapportagedatum (researchReportDate) bevat.

    Document is in overtreding wanneer researchReportDate niet bestaat of niet gevuld is.
    """
    __feedbackMessage = "%s"
    __explanation = "Controleert of het brondocument een rapportagedatum (researchReportDate) bevat."
    code = "02"
    name = "Rapportagedatum"
    object_type = "BHR-GT"

    def __init__(self, emergence=enums.Importance.INFO):
        super().__init__(
            self.code,
            self.name,
            self.object_type,
            emergence,
            self.__feedbackMessage,
            self.__explanation,
            self.__docstring,
        )

    def applyRule(self, doc):
        research_report_date = doc.get_element_from_metadata("researchReportDate")
        if not research_report_date:
            specific_feedbackmessage = (
                "Document bevat geen rapportagedatum (researchReportDate)."
            )
            return self.getFeedbackMessage() % specific_feedbackmessage
        elif not research_report_date.get("date"):
            specific_feedbackmessage = "Document bevat een rapportagedatum (researchReportDate) maar die is niet ingevuld."
            return self.getFeedbackMessage() % specific_feedbackmessage
        else:
            return None
