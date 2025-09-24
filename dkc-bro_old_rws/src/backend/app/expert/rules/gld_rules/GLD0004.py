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

    __feedbackMessage = (
        "Meting(en): '%s' zijn meer dan 20 dagen geleden ingewonnen: '%s'."
    )
    __explanation = "Controleert of alle aangeboden metingen niet eerder dan 20 dagen geleden zijn ingewonnen."
    code = "04"
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
            for index, rt in enumerate(
                result_times, start=1
            ):  # Start 1 so the feedbackMessage doesnt use python indexing.
                time_instant = doc.get_child_element_by_tag_name(rt, "TimeInstant")
                time_position = doc.get_child_element_by_tag_name(
                    time_instant, "timePosition"
                )
                time_position_dt = datetime.fromisoformat(time_position.text)
                if (
                    time_position_dt.timestamp()
                    < (now - timedelta(days=20)).timestamp()
                ):
                    formatted_time_position = time_position_dt.strftime(
                        "%d-%m-%Y %H:%M"
                    )
                    faulty_result_times.append((index, formatted_time_position))
                # if (
                #     datetime.fromisoformat(time_position.text).timestamp()
                #     < (now - timedelta(days=20)).timestamp()
                # ):
                #     faulty_result_times.append((index, time_position.text))

            if faulty_result_times:
                indices, values = zip(*faulty_result_times)
                return self.getFeedbackMessage() % (
                    ", ".join(map(str, indices)),
                    ", ".join(values),
                )
            else:
                return None
