import numpy as np

# Imports from generic component
import app.enums as enums
import app.utils.enums as rws_enums
import app.utils.putils as putils


class rule6705:
    __docstring = ""
    __feedbackMessage = "In de %s regels met meetwaarden is Conuspenetratietest gecorrigeerde conusweerstand (correctedConeResistance) %s keer niet ingevuld."
    __explanation = "Controleert hoeveel meetwaardes van de gecorrigeerde conusweerstand (correctedConeResistance) niet is ingevuld van een CPT"
    code = 6705
    name = "Gecorrigeerde conusweerstand"
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
        (index, paramName) = rws_enums.CPTParams.CORRECTEDCONERESISTANCE.value
        if putils.cpt_parameters_filled(doc.get_cpt_parameters_map(), paramName):
            cptMatrix = doc.get_cpt_matrix()
            result = np.where(cptMatrix[:, index] == rws_enums.MISSINGVALUE)
            if result[0].size != 0:
                return self.getFeedbackMessage() % (cptMatrix.shape[0], result[0].size)
        return None
