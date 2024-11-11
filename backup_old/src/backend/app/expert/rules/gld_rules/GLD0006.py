# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule
from app.utils.parser_utils import XLINKHREF


class GLD0006(superRule):
    __docstring = """
    Controleregel GLD0006 controleert of de meetprocedure voor alle aangeboden metingen de RWS-meetprocedure (RWSgwmon) is."
    Om dit te controleren worden de velden ObservationProcess => processReference gebruikt.

    Document is in overtreding wanneer de meetprocedure niet voor alle metingen gelijk is aan (RWSgwmon).
    """

    __feedbackMessage = "Gebruikte meetprocedure is niet gelijk aan de RWS-meetprocedure (RWSgwmon) voor alle aangeboden metingen."
    __explanation = "Controleert of de RWS-meetprocedure (RWSgwmon) is gebruikt voor de aangeboden metingen."
    code = "6"
    name = "Meetprocedure"
    object_type = "GLD"

    def __init__(self, emergence=enums.Importance.ERROR):
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
        faulty_procedure = False
        observation_processes = doc.get_list_of_elements_by_tag_name(
            "ObservationProcess"
        )
        if observation_processes:
            for op in observation_processes:
                reference = doc.get_child_element_by_tag_name(op, "processReference")
                if not reference.attrib[XLINKHREF].endswith("RWSgwmon"):
                    faulty_procedure = True
                    break
        return self.getFeedbackMessage() if faulty_procedure else None
