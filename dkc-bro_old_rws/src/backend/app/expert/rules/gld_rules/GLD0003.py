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

    __feedbackMessage = "Aangeboden meting(en) met ID: '%s' liggen in de toekomst. Vandaag is: '%s'."  # 1 of meerdere aangeboden metingen liggen in de toekomst
    __explanation = "Controleert of alle aangeboden metingen in het verleden liggen."
    code = "03"
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
        ##TODO: check what we can use as ID if we have multiple phenomenonTime entries. or do the files only ever have 1? (i.e. each xml file only has 1 instance)
        now = datetime.now()
        phenomenom_times = doc.get_list_of_elements_by_tag_name("phenomenonTime")
        future_dates = []
        if phenomenom_times:
            for i, pt in enumerate(phenomenom_times):
                time_period = doc.get_child_element_by_tag_name(pt, "TimePeriod")
                end_date = doc.get_child_element_by_tag_name(time_period, "endPosition")
                end_date_datetime = datetime.fromisoformat(end_date.text)
                if end_date_datetime > now:
                    future_dates.append(str(i + 1))

        if future_dates:
            future_dates_str = ", ".join(future_dates)
            return self.getFeedbackMessage() % (
                future_dates_str,
                now.strftime("%d-%m-%Y %H:%M"),
            )
        else:
            return None
