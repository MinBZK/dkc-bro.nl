import numpy as np

# Imports from generic component
import app.enums as enums
import app.utils.enums as rws_enums


class rule6903:

    __feedbackMessage = "In de %s regels met meetwaarden is Dissipatietest waterspanning u1 (porePressureU1) %s keer niet ingevuld."
    __explanation = "Controleert hoeveel meetwaardes van de waterspanning u1 (porePressureU1) niet is ingevuld van een dissipatietest"
    code = 6903
    name = "Waterspanning U1"
    object_type = "CPT"

    def __init__(self, emergence=enums.Importance.INFO):
        super().__init__(
            self.code,
            self.name,
            self.object_type,
            emergence,
            self.__feedbackMessage,
            self.__explanation,
        )

    def applyRule(self, doc):
        dissipationMatrices = doc.get_dissipation()
        dissResultString = ""
        if dissipationMatrices is None:
            return None
        for i, dissMatrix in enumerate(dissipationMatrices, 1):
            result = np.where(
                dissMatrix[:, rws_enums.DissipationtestParams.WATERSPANNINGU1]
                == rws_enums.MISSINGVALUE
            )
            if result[0].size != 0:
                dissResultString += f"Dissipatietest #{i}: {self.getFeedbackMessage() % (dissMatrix.shape[0], result[0].size)}. "
        if len(dissResultString) == 0:
            return None
        return dissResultString
