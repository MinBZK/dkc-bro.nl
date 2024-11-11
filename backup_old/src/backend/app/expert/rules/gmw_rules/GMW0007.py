# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0007(superRule):
    __docstring = """
    Controleregel GMW0007 controleert of alle peilbuizen in de GMW een filterkous bevatten.
    Om dit te controleren wordt gekeken naar het veld sockMaterial en de vulling hiervan.

    Document is in overtreding wanneer niet alle peilbuizen in het object een filterkous bevatten.
    """

    __feedbackMessage = "Een of meer peilbuizen heeft geen filterkous."
    __explanation = (
        "Regel die controleert of alle peilbuizen in de GMW een filterkous hebben."
    )
    code = 7
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

    def __validate_sock_material(self, doc):
        tube_sock_materials = doc.get_list_of_elements_by_tag_name("sockMaterial")
        return all([tsm.text != "geen" for tsm in tube_sock_materials])

    def applyRule(self, doc):
        return (
            self.getFeedbackMessage()
            if (not self.__validate_sock_material(doc))
            else None
        )
