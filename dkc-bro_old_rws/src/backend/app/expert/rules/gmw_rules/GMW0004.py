# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0004(superRule):
    __docstring = """
    Controleregel GMW0004 controleert of de Nauwkeurigheid horizontale positiebepaling (horizontalPositioningMethod) nauwkeurig genoeg is.
    Geldige waardes zijn "RTKGPS0tot2cm","RTKGPS2tot5cm","RTKGPS5tot10cm","tachymetrie0tot10cm",

    Document is in overtreding wanneer de nauwkeurigheid niet voldoet aan de gewenste naurwkeurigheid.
    """

    __feedbackMessage = "Nauwkeurigheid horizontale positiebepaling is niet nauwkeurig genoeg. De gevonden waarde is: '%s'."
    __explanation = "Regel die controleert of de nauwkeurigheid horizontale positiebepaling voldoet aan de kwaliteitseisen"
    code = "04"
    name = "Nauwkeurigheid horizontale positiebepaling"
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
        # Get data and validate
        horizontal_positioning = doc.get_element_from_metadata(
            "horizontalPositioningMethod"
        )
        valid_position = [
            "RTKGPS0tot2cm",
            "RTKGPS2tot5cm",
            "RTKGPS5tot10cm",
            "tachymetrie0tot10cm",
        ]

        if horizontal_positioning not in valid_position:
            return self.getFeedbackMessage() % horizontal_positioning
        else:
            return None
