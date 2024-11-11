import re

from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GEN1(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GEN1 controleert of het veld Object-id bronhouder (objectIdAccountableParty) voldoet aan het
        format afgesproken met RWS. Deze format is als volgt:
        [WBS-nummer X.xxxxxxxx.xxxx]-[zaaknummer RWS xxxxxxxx]-[specificatie RWS]-[referentie ON],
        voorbeeld: [P.00000183.0002]-[31168417]-[A15-15.2xx-S-05]-[referentie ON].
        Het objectIdAccountableParty wordt door middel van XML-parsing uit het brondocument gelezen en tegen een
        Reguliere Expressie aangehouden die de geldigheid controleert.
        """,
        feedback_message="""
        Object-id bronhouder (objectIdAccountableParty) voldoet niet aan het afgesproken format.
        De werkelijke object-id uit de xml is %s
        """,
        explanation=""""
        Controleert of het Object-id bronhouder (objectIdAccountableParty) voldoet aan het format zoals
        gevraagd door RWS.""",
        code="01",
        name="Object-id bronhouder",
        object_type=ObjectType.GEN,
    )

    @staticmethod
    def check_object_id_accountable_party(object_id: str) -> bool:
        pattern = r"(\[?[a-zA-Z]\.\d{6}(?:\d{2})?\.?\d{0,4}\]?)-(\[?\d{8}]?(?:-.*?)?\]?)$"
        return bool(re.match(pattern, object_id))

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        object_id = payload.get_element_from_metadata("objectIdAccountableParty")

        if not object_id or not self.check_object_id_accountable_party(object_id):
            feedback_message = self.rule_info.feedback_message % object_id
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
