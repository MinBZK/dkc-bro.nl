from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW4(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW4 controleert of de Nauwkeurigheid horizontale positiebepaling (horizontalPositioningMethod) nauwkeurig genoeg is.
        Geldige waardes zijn "RTKGPS0tot2cm","RTKGPS2tot5cm","RTKGPS5tot10cm","tachymetrie0tot10cm",

        Document is in overtreding wanneer de nauwkeurigheid niet voldoet aan de gewenste naurwkeurigheid.
        """,
        feedback_message="Nauwkeurigheid horizontale positiebepaling is niet nauwkeurig genoeg. De gevonden waarde is: '%s'.",
        explanation="Regel die controleert of de nauwkeurigheid horizontale positiebepaling voldoet aan de kwaliteitseisen",
        code="04",
        name="Nauwkeurigheid horizontale positiebepaling",
        object_type=ObjectType.GMW,
    )

    valid_positions = [
        "RTKGPS0tot2cm",
        "RTKGPS2tot5cm",
        "RTKGPS5tot10cm",
        "tachymetrie0tot10cm",
    ]

    @classmethod
    def check_horizontal_positioning(cls, payload: XmlParser):
        horizontal_positioning = payload.get_element_from_metadata("horizontalPositioningMethod")

        if horizontal_positioning not in cls.valid_positions:
            return horizontal_positioning
        return ""

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        invalid_positioning = self.check_horizontal_positioning(payload)

        if invalid_positioning:
            feedback_message = self.rule_info.feedback_message % invalid_positioning
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
