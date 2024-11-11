# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class BHRGT0007(superRule):
    __docstring = """
    Controleregel BHRGT0007 controleert of de beschrijfprocedure (descriptionProcedure) van het document volgens ISO14688 is.

    Document is in overtreding wanneer beschrijfprocedure (descriptionProcedure) van het document niet gelijk is aan een van de geldige ISO14688 waarden.
    """
    __feedbackMessage = "De beschrijfprocedure (descriptionProcedure) van het document is niet volgens ISO14688."
    __explanation = "Controleert of de beschrijfprocedure (descriptionProcedure) van het document ISO14688 volgt."
    code = 7
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
        self.valid_procedures = [
            "ISO14688d1v2019c2020",
            "ISO14688d1v2019c2020enISO14689d1v2018",
        ]

    def applyRule(self, doc):
        description_procedure = doc.get_element_from_metadata("descriptionProcedure")
        return (
            self.getFeedbackMessage()
            if (
                description_procedure
                and description_procedure not in self.valid_procedures
            )
            else None
        )
