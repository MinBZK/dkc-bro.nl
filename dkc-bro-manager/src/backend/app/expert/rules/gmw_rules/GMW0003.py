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

    __feedbackMessage = "Nauwkeurigheid verticale positiebepaling is niet nauwkeurig genoeg voor peilbuizen en/of maaiveld."  # %s
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

        # def applyRule(self, doc):

    #     # Get necessary values
    #     monitoring_tube = [id for id in doc.get_list_of_elements_by_tag_name("monitoringTube")]
    #     tube_id = int(doc.get_child_element_by_tag_name(monitoring_tube, "tubeNumber").text)
    #     tube_top_positioning_method = doc.get_element_from_metadata("tubeTopPositioningMethod")
    #     ground_level_positioning_method = doc.get_element_from_metadata("groundLevelPositioningMethod")

    #     # Validity check
    #     peilbuizen_valid = tube_top_positioning_method in ["RTKGPS0tot4cm", "waterpassing0tot2cm"]
    #     maaiveld_valid = ground_level_positioning_method in ["RTKGPS0tot4cm", "waterpassing0tot2cm", "waterpassing2tot4cm"]

    #     if not peilbuizen_valid:
    #         specific_message = f"Nauwkeurigheid verticale positiebepaling voor peilbuis(zen) {tube_id} is niet nauwkeurig genoeg. De gevonden waarde is '{tube_top_positioning_method}'."
    #         return self.getFeedbackMessage() % specific_message

    #     if not maaiveld_valid:
    #         specific_message = f"Nauwkeurigheid verticale positiebepaling is niet nauwkeurig genoeg voor het maaiveld. De gevonden waarde is '{ground_level_positioning_method}'."
    #         return self.getFeedbackMessage() % specific_message

    #     if not all([peilbuizen_valid, maaiveld_valid]):
    #         specific_message = f"Nauwkeurigheid verticale positiebepaling voor maaiveld en peilbuis(zen) {tube_id} is niet nauwkeurig genoeg. De gevonden waarden zijn '{ground_level_positioning_method}', '{tube_top_positioning_method}' respectievelijk."
    #         return self.getFeedbackMessage() % specific_message
    #     else:
    #         return None
