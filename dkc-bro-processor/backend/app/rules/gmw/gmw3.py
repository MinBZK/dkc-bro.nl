from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW3(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW3 controleert of de Nauwkeurigheid verticale positiebepaling nauwkeurig genoeg is voor peilbuizen en maaiveld.
        Geldige waardes voor peilbuizen (tubeTopPositioningMethod) zijn "RTKGPS0tot4cm" en "waterpassing0tot2cm".
        Geldige waardes voor maaiveld (groundLevelPositioningMethod) zijn "RTKGPS0tot4cm", "waterpassing0tot2cm", "waterpassing2tot4cm",

        Document is in overtreding wanneer de nauwkeurigheid van peilbuizen of maaiveld niet allemaal voldoen aan de gewenste
        naurwkeurigheid.
        """,
        feedback_message="%s",
        explanation="Controleert de nauwkeurigheid van de verticale positiebepaling van peilbuizen en maaiveld.",
        code="03",
        name="Nauwkeurigheid verticale positie",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def check_vertical_positioning(payload: XmlParser) -> str:
        monitoring_tubes = payload.get_list_of_elements_by_tag_name("monitoringTube") or []
        tube_top_positioning_method = payload.get_element_from_metadata("tubeTopPositioningMethod")
        ground_level_positioning_method = payload.get_element_from_metadata("groundLevelPositioningMethod")

        valid_tube_methods = ["RTKGPS0tot4cm", "waterpassing0tot2cm"]
        valid_ground_methods = [
            "RTKGPS0tot4cm",
            "waterpassing0tot2cm",
            "waterpassing2tot4cm",
        ]

        for tube in monitoring_tubes:
            tube_number = payload.get_child_element_by_tag_name(tube, "tubeNumber")
            if tube_number is None or tube_number.text is None:
                continue
            tube_id = int(tube_number.text)

            peilbuizen_valid = tube_top_positioning_method in valid_tube_methods
            maaiveld_valid = ground_level_positioning_method in valid_ground_methods

            if not peilbuizen_valid:
                return f"Nauwkeurigheid verticale positiebepaling voor peilbuis(zen) {tube_id} is niet nauwkeurig genoeg. \
                        De gevonden waarde is '{tube_top_positioning_method}'."

            if not maaiveld_valid:
                return f"Nauwkeurigheid verticale positiebepaling is niet nauwkeurig genoeg voor het maaiveld. \
                        De gevonden waarde is '{ground_level_positioning_method}'."

            if not all([peilbuizen_valid, maaiveld_valid]):
                return f"Nauwkeurigheid verticale positiebepaling voor maaiveld en peilbuis(zen) {tube_id} is niet nauwkeurig genoeg. \
                        De gevonden waarden zijn '{ground_level_positioning_method}', '{tube_top_positioning_method}' respectievelijk."

        return ""

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        error_message = self.check_vertical_positioning(payload)

        if error_message:
            feedback_message = self.rule_info.feedback_message % error_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
