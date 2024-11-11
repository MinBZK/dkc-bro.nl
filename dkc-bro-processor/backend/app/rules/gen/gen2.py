from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GEN2(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GEN2 controleert of het kwaliteitsregime (qualityRegime) gelijk is aan IMBRO.
        qualityRegime wordt door middel van XML-parsing uit het brondocument gelezen en vergeleken met de waarde "IMBRO".

        Document is in overtreding wanneer de uitgelezen waarde niet gelijk is aan "IMBRO".
        """,
        feedback_message="Kwaliteitsregime (qualityRegime) is niet gelijk aan IMBRO. De gevonden waarde is '%s'.",
        explanation="Controleert of het kwaliteitsregime (qualityRegime) gelijke is aan IMBRO.",
        code="02",
        name="Kwaliteitsregime",
        object_type=ObjectType.GEN,
    )

    @staticmethod
    def check_quality_regime(quality_regime: str) -> bool:
        return quality_regime == "IMBRO"

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        quality_regime = payload.get_element_from_metadata("qualityRegime")

        if not quality_regime or not self.check_quality_regime(quality_regime):
            feedback_message = self.rule_info.feedback_message % quality_regime
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
