# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0003(superRule):
    __docstring = """
    Controleregel GMW0003 controleert of de Nauwkeurigheid verticale positiebepaling nauwkeurig genoeg is voor peilbuizen en maaiveld.
    Geldige waardes voor peilbuizen (tubeTopPositioningMethod) zijn "RTKGPS0tot4cm" en "waterpassing0tot2cm".
    Geldige waardes voor maaiveld (groundLevelPositioningMethod) zijn "RTKGPS0tot4cm", "waterpassing0tot2cm", "waterpassing2tot4cm",

    Document is in overtreding wanneer de nauwkeurigheid van peilbuizen of maaiveld niet allemaal voldoen aan de gewenste naurwkeurigheid.
    """

    __feedbackMessage = "Nauwkeurigheid verticale positiebepaling is niet nauwkeurig genoeg voor peilbuizen en/of maaiveld."
    __explanation = "Controleert de nauwkeurigheid van de verticale positiebepaling van peilbuizen en maaiveld."
    code = 3
    name = "Nauwkeurigheid verticale positie"
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

    def __validate_ground_level(self, doc):
        groundLevelPositioningMethod = doc.get_element_from_metadata(
            "groundLevelPositioningMethod"
        )
        return groundLevelPositioningMethod in [
            "RTKGPS0tot4cm",
            "waterpassing0tot2cm",
            "waterpassing2tot4cm",
        ]

    def __validate_tubes(self, doc):
        tube_positioning_methods = doc.get_list_of_elements_by_tag_name(
            "tubeTopPositioningMethod"
        )
        return all(
            tpm.text in ["RTKGPS0tot4cm", "waterpassing0tot2cm"]
            for tpm in tube_positioning_methods
        )

    def applyRule(self, doc):
        ground_level_valid = self.__validate_ground_level(doc)
        tubes_valid = self.__validate_tubes(doc)
        return (
            self.getFeedbackMessage()
            if (not all([ground_level_valid, tubes_valid]))
            else None
        )
