from datetime import datetime

# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GLD0003(superRule):
    __docstring = """
    Controleregel GLD0003 controleert of alle aangeboden metingen in het verleden liggen.
    Om dit te controleren worden de velden phenomenonTime => TimePeriod => endPosition gebruikt.

    Document is in overtreding wanneer een of meer aangeboden metingen in de toekomst liggen.
    """

    __feedbackMessage = "1 of meerdere aangeboden metingen liggen in de toekomst"
    __explanation = "Controleert of alle aangeboden metingen in het verleden liggen."
    code = "3"
    name = "Observatieperiode"
    object_type = "GLD"

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
        now = datetime.now()
        phenomenom_times = doc.get_list_of_elements_by_tag_name("phenomenonTime")
        faulty_end_date = False
        if phenomenom_times:
            for pt in phenomenom_times:
                time_period = doc.get_child_element_by_tag_name(pt, "TimePeriod")
                end_date = doc.get_child_element_by_tag_name(time_period, "endPosition")
                if datetime.fromisoformat(end_date.text) > now:
                    faulty_end_date = True
                    break

        return self.getFeedbackMessage() if faulty_end_date else None
