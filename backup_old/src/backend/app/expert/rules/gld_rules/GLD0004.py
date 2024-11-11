from datetime import datetime, timedelta

# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GLD0004(superRule):
    __docstring = """
    Controleregel GLD0004 controleert of alle aangeboden metingen in de laatste 20 dagen zijn aangeboden.
    Om dit te controleren worden de velden resultTime => TimeInstant => timePosition gebruikt.

    Document is in overtreding wanneer een of meer aangeboden metingen niet in de laatste 20 dagen zijn aangeboden.
    """

    __feedbackMessage = "1 of meerdere aangeboden metingen zijn meer dan 20 dagen geleden ingewonnen: %s"
    __explanation = "Controleert of alle aangeboden metingen niet eerder dan 20 dagen geleden zijn ingewonnen."
    code = "4"
    name = "Tijdstip resultaat"
    object_type = "GLD"

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

    def applyRule(self, doc):
        now = datetime.now()
        result_times = doc.get_list_of_elements_by_tag_name("resultTime")
        faulty_result_times = []
        if result_times:
            for rt in result_times:
                time_instant = doc.get_child_element_by_tag_name(rt, "TimeInstant")
                time_position = doc.get_child_element_by_tag_name(
                    time_instant, "timePosition"
                )
                if (
                    datetime.fromisoformat(time_position.text).timestamp()
                    < (now - timedelta(days=20)).timestamp()
                ):
                    faulty_result_times.append(time_position.text)
                    break

        return (
            self.getFeedbackMessage() % (",".join(faulty_result_times))
            if len(faulty_result_times) > 0
            else None
        )
