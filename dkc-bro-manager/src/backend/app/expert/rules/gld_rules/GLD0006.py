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

    __feedbackMessage = "Gebruikte meetprocedure is niet gelijk aan de RWS-meetprocedure (RWSgwmon) voor de meting(en) met ID: '%s'. De gevonden waarde is: '%s'."
    __explanation = "Controleert of de RWS-meetprocedure (RWSgwmon) is gebruikt voor de aangeboden metingen."
    code = "06"
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
        faulty_procedures = []
        observation_processes = doc.get_list_of_elements_by_tag_name(
            "ObservationProcess"
        )

        if observation_processes:
            for index, op in enumerate(observation_processes):
                reference = doc.get_child_element_by_tag_name(op, "processReference")
                href_value = reference.attrib[XLINKHREF]
                href_value = href_value.split(":")[-1]
                if not href_value.endswith("RWSgwmon"):
                    faulty_procedures.append((index + 1, href_value))
        if faulty_procedures:
            messages = []
            for index, href_value in faulty_procedures:
                messages.append(self.__feedbackMessage % (index, href_value))
            return "\n".join(messages)
        else:
            return None
