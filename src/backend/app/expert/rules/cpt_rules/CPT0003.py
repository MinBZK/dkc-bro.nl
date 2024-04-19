import numpy as np

# Imports from generic component
import app.enums as enums
import app.utils.enums as rws_enums
import app.utils.putils as putils
from app.expert.rules._superrule import superRule


class CPT0003(superRule):
    __docstring = """
    Controleregel CPT0003 controleert of de Conuspenetratietest hellingsresultante (inclinationResultant) is ingevuld in iedere meetwaarde in de CPT. Wanneer deze niet
    in iedere meetwaarde is ingevuld, zal de controleregel bijhouden voor hoeveel meetwaarden dit niet is gedaan.

    Document is in overtreding wanneer Conuspenetratietest hellingsresultante (inclinationResultant) niet in iedere regel is ingevuld.
    """
    __feedbackMessage = "In de %s regels met meetwaarden is Conuspenetratietest hellingsresultante (inclinationResultant) %s keer niet ingevuld."
    __explanation = "Controleert hoeveel meetwaardes van de hellingsresultante (inclinationResultant) niet is ingevuld van een CPT"
    code = "3"
    name = "Hellingsresultante"
    object_type = "CPT"

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
        (index, paramName) = rws_enums.CPTParams.INCLINATIONRESULTANT.value
        if putils.cpt_parameters_filled(doc.get_cpt_parameters_map(), paramName):
            cptMatrix = doc.get_cpt_matrix()
            result = np.where(cptMatrix[:, index] == rws_enums.MISSINGVALUE)
            if result[0].size != 0:
                return self.getFeedbackMessage() % (cptMatrix.shape[0], result[0].size)
        return None
