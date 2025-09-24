# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0007(superRule):
    __docstring = """
    Controleregel GMW0007 controleert of alle peilbuizen in de GMW een filterkous bevatten.
    Om dit te controleren wordt gekeken naar het veld sockMaterial en de vulling hiervan.

    Document is in overtreding wanneer niet alle peilbuizen in het object een filterkous bevatten.
    """

    __feedbackMessage = "Peilbuis(zen) met ID: '%s' heeft/hebben geen filterkous."
    __explanation = (
        "Regel die controleert of alle peilbuizen in de GMW een filterkous hebben."
    )
    code = "07"
    name = "Filterkous"
    object_type = "GMW"

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
        # Validate sock material
        tube_sock_materials = doc.get_list_of_elements_by_tag_name("sockMaterial")
        faulty_tubes = []

        for index, tsm in enumerate(
            tube_sock_materials, start=1
        ):  # xml files dont start at index 0
            if tsm.text == "geen":
                faulty_tubes.append(str(index))

        if faulty_tubes:
            return self.getFeedbackMessage() % ", ".join(faulty_tubes)
        else:
            return None
