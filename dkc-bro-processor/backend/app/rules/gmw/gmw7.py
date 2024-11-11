from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW7(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW7 controleert of alle peilbuizen in de GMW een filterkous bevatten.
        Om dit te controleren wordt gekeken naar het veld sockMaterial en de vulling hiervan.

        Document is in overtreding wanneer niet alle peilbuizen in het object een filterkous bevatten.
        """,
        feedback_message="Peilbuis(zen) met ID: '%s' heeft/hebben geen filterkous.",
        explanation="Regel die controleert of alle peilbuizen in de GMW een filterkous hebben.",
        code="07",
        name="Filterkous",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def check_sock_material(payload: XmlParser) -> list:
        tube_sock_materials = payload.get_list_of_elements_by_tag_name("sockMaterial") or []
        faulty_tubes = []

        for index, tsm in enumerate(tube_sock_materials, start=1):
            if tsm.text == "geen":
                faulty_tubes.append(str(index))

        return faulty_tubes

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        faulty_tubes = self.check_sock_material(payload)

        if faulty_tubes:
            feedback_message = self.rule_info.feedback_message % ", ".join(faulty_tubes)
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
