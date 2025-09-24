import numpy as np

# Imports from generic component
import app.enums as enums
import app.utils.enums as rws_enums
import app.utils.putils as putils
from app.expert.rules._superrule import superRule


class CPT0004B(superRule):
    __docstring = """
    Controleregel CPT0004B controleert of de Conuspenetratietest plaatselijke wrijving (localFriction) is ingevuld in iedere meetwaarde 
    in de CPT behalve de laatste 30 cm van de sondeertraject lengte. Wanneer deze niet in iedere meetwaarde is ingevuld, zal de 
    controleregel bijhouden voor hoeveel meetwaarden dit niet is gedaan.

    Document is in overtreding wanneer Conuspenetratietest plaatselijke wrijving (localFriction) niet in iedere regel is ingevuld.
    """
    __feedbackMessage = "In de %s regels met meetwaarden is Conuspenetratietest plaatselijke wrijving (localFriction) %s keer niet ingevuld behalve de laatste 30 cm."
    __explanation = "Controleert hoeveel meetwaardes van de plaatselijke wrijving (localFriction) niet is ingevuld van een CPT behalve de laatste 30 cm"
    code = "04B"
    name = "Plaatselijke wrijving"
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
        (index, paramName) = rws_enums.CPTParams.LOCALFRICTION.value
        if putils.cpt_parameters_filled(doc.get_cpt_parameters_map(), paramName):
            cptMatrix = doc.get_cpt_matrix()
            result = np.where(
                cptMatrix[
                    np.where(
                        cptMatrix[:, rws_enums.CPTParams.PENETRATIONLENGTH.value[0]]
                        < cptMatrix[-1, rws_enums.CPTParams.PENETRATIONLENGTH.value[0]]
                        - rws_enums.PENETRATIONLENGTH_NOT_IN_SCOPE
                    ),
                    index,
                ]
                == rws_enums.MISSINGVALUE
            )
            if result[0].size != 0:
                return self.getFeedbackMessage() % (cptMatrix.shape[0], result[0].size)
        return None
