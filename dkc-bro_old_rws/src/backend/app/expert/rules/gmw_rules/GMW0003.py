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

    __feedbackMessage = "%s"
    __explanation = "Controleert de nauwkeurigheid van de verticale positiebepaling van peilbuizen en maaiveld."
    code = "03"
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

    def applyRule(self, doc):
        monitoring_tubes = doc.get_list_of_elements_by_tag_name("monitoringTube")
        tube_top_positioning_method = doc.get_element_from_metadata(
            "tubeTopPositioningMethod"
        )
        ground_level_positioning_method = doc.get_element_from_metadata(
            "groundLevelPositioningMethod"
        )

        for tube in monitoring_tubes:
            tube_ids = int(doc.get_child_element_by_tag_name(tube, "tubeNumber").text)

            # Validity check
            peilbuizen_valid = tube_top_positioning_method in [
                "RTKGPS0tot4cm",
                "waterpassing0tot2cm",
            ]
            maaiveld_valid = ground_level_positioning_method in [
                "RTKGPS0tot4cm",
                "waterpassing0tot2cm",
                "waterpassing2tot4cm",
            ]

            if not peilbuizen_valid:
                specific_message = f"Nauwkeurigheid verticale positiebepaling voor peilbuis(zen): '{tube_ids}' is niet nauwkeurig genoeg. De gevonden waarde is: '{tube_top_positioning_method}'."
                return self.getFeedbackMessage() % specific_message

            if not maaiveld_valid:
                specific_message = f"Nauwkeurigheid verticale positiebepaling is niet nauwkeurig genoeg voor het maaiveld. De gevonden waarde is: '{ground_level_positioning_method}'."
                return self.getFeedbackMessage() % specific_message

            if not all([peilbuizen_valid, maaiveld_valid]):
                specific_message = f"Nauwkeurigheid verticale positiebepaling voor maaiveld en peilbuis(zen): '{tube_ids}' is niet nauwkeurig genoeg. De gevonden waarden zijn: '{ground_level_positioning_method}', '{tube_top_positioning_method}' respectievelijk."
                return self.getFeedbackMessage() % specific_message

        # If all tubes are valid, return None
        return None
