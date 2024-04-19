# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0008(superRule):
    __docstring = """
    Controleregel GMW0008 controleert of alle peilbuizen bestaan uit materialen geschikt voor het doen van kwaliteitsmetingen.
    Om dit te controleren wordt gekeken naar de velden initialFunction, tubeMaterial, glue en de vulling hiervan.
    Als de initialFunction kwaliteit of kwaliteitStand is moet er lijm aanwezig zijn in de peilbuis.
    Daarnaast mag het materiaal van de buis dan niet voorkomen in "peHighDensity", "pvc" of "teflon".

    Document is in overtreding wanneer niet alle peilbuizen bestaan uit de juiste materialen volgens bovenstaande regels.
    """

    __feedbackMessage = "De gebruikte materialen voor een of meerdere buizen voldoen niet voor kwaliteitsmetingen."
    __explanation = "Deze regel controleert of de gebruikte materialen voldoen aan de eisen voor kwaliteitsmetingen indien van toepassing."
    code = 8
    name = "Gebruikte materialen buis"
    object_type = "GMW"

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

    def __validate_materials(self, doc):
        initial_function = doc.get_element_by_tag_name("initialFunction").text
        for monitoring_tube in doc.get_list_of_elements_by_tag_name("monitoringTube"):
            glue = doc.get_child_element_by_tag_name(monitoring_tube, "glue").text
            tube_material = doc.get_child_element_by_tag_name(
                monitoring_tube, "tubeMaterial"
            ).text
            if initial_function in ["kwaliteit", "kwaliteitStand"] and (
                glue == "ongespecificeerd"
                or tube_material in ["peHighDensity", "pvc", "teflon"]
            ):
                return False
        return True

    def applyRule(self, doc):
        return (
            self.getFeedbackMessage() if (not self.__validate_materials(doc)) else None
        )
