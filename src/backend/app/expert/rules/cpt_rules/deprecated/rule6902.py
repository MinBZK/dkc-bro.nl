import numpy as np

# Imports from generic component
import app.enums as enums
import app.utils.enums as rws_enums


class rule6902:

    __feedbackMessage = "In de %s regels met meetwaarden is Dissipatietest Conusweerstand (coneResistance) %s keer niet ingevuld."
    __explanation = "Controleert hoeveel meetwaardes van de conusweerstand (coneResistance) niet is ingevuld van een dissipatietest"
    code = 6902
    name = "Dissipatietest Conusweerstand"
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
        if dissipationMatrices is None:
            return None
        dissResultString = ""
        for i, dissMatrix in enumerate(dissipationMatrices, 1):
            result = np.where(
                dissMatrix[:, rws_enums.DissipationtestParams.CONUSWEERSTAND]
                == rws_enums.MISSINGVALUE
            )
            if result[0].size != 0:
                dissResultString += f"Dissipatietest #{i}: {self.getFeedbackMessage() % (dissMatrix.shape[0], result[0].size)}. "
        if len(dissResultString) == 0:
            return None
        return dissResultString
