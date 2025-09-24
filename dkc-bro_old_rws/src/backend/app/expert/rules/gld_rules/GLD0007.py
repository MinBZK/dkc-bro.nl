# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule
from app.utils.parser_utils import XLINKHREF


class GLD0007(superRule):
    __docstring = """
    Controleregel GLD0007 controleert of de beoordelingsprocedure voor alle aangeboden metingen volgens het QC-Protocol (PMBProtocolDatakwaliteitscontroleQC2018v2.0) is
    Om dit te controleren worden de velden ObservationProcess, parameter, named value, name, value gebruikt.

    Document is in overtreding wanneer de beoordelingsprocedure niet voor alle metingen gelijk is aan QC-Protocol (PMBProtocolDatakwaliteitscontroleQC2018v2.0).
    """

    __feedbackMessage = "Gebruikte beoordelingsprocedure is niet volgens het QC-Protocol voor meting(en) met ID: '%s'. De gevonden waarde is: '%s'."
    __explanation = "Controleert of de kwaliteitsborging van alle metingen is gedaan volgens het QC-Protocol."
    code = "07"
    name = "Beoordelingsprocedure"
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
        observation_processes = doc.get_list_of_elements_by_tag_name(
            "ObservationProcess"
        )
        violated_instances = []

        if observation_processes:
            for index, op in enumerate(observation_processes, start=1):
                parameters = doc.get_child_elements_by_tag_name(op, "parameter")
                for p in parameters:
                    named_value = doc.get_child_element_by_tag_name(p, "NamedValue")
                    name = doc.get_child_element_by_tag_name(named_value, "name")
                    value = doc.get_child_element_by_tag_name(named_value, "value")
                    if (
                        name.attrib[XLINKHREF]
                        == "urn:bro:gld:ObservationProcess:evaluationProcedure"
                        and value.text != "PMBProtocolDatakwaliteitscontroleQC2018v2.0"
                    ):
                        violated_instances.append((index, value.text))
            if violated_instances:
                indices, values = zip(*violated_instances)
                return self.getFeedbackMessage() % (
                    ", ".join(map(str, indices)),
                    ", ".join(values),
                )
            else:
                return None
