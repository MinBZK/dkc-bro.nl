# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BHRGT0007(superRule):
    __docstring = """
    Controleregel BHRGT0007 controleert of de beschrijfprocedure (descriptionProcedure) van het document volgens ISO14688 is.

    Document is in overtreding wanneer beschrijfprocedure (descriptionProcedure) van het document niet de waarde '14688' bevat.
    """
    __feedbackMessage = "De beschrijfprocedure (descriptionProcedure) van het document bevat niet de waarde '14688'. De gevonden waarde is '%s'"
    __explanation = "Controleert of de beschrijfprocedure (descriptionProcedure) van het document de waarde '14688' bevat."
    code = "07"
    name = "Beschrijfprocedure"
    object_type = "BHR-GT"

    def __init__(self, emergence=enums.Importance.WARNING):
        super().__init__(
            self.code,
            self.name,
            self.object_type,
            emergence,
            self.__feedbackMessage,
            self.__explanation,
            self.__docstring,
        )
        self.valid_procedure: str = "14688"

    def applyRule(self, doc):
        description_procedure = doc.get_element_from_metadata("descriptionProcedure")
        if description_procedure and self.valid_procedure not in description_procedure:
            return self.getFeedbackMessage() % description_procedure
        else:
            return None
