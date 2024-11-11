from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult
from app.utils.parser_utils import XLINKHREF


class GLD8(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GLD8 controleert of de status van kwaliteitscontrole voor alle aangeboden metingen of goedgekeurd is of nog niet
        beoordeeld. Om dit te controleren worden de velden TVPMeasurementMetadata, qualifier, Category, codeSpace, value gebruikt.

        Document is in overtreding wanneer de status van kwaliteitscontrole niet voor alle metingen goedgekeurd is of nog niet beoordeeld.
        """,
        feedback_message="""
        De status van kwaliteitscontrole van een of meerdere metingen is niet gelijk aan goedgekeurd of nog niet beoordeeld.
        Gevonden waarden: %s.
        """,
        explanation="""
        Controleert of de status van kwaliteitscontrole gelijk is aan goedgekeurd of nog niet beoordeeld voor alle aangeleverde
        metingen.
        """,
        code="08",
        name="Statuskwaliteitscontrole",
        object_type=ObjectType.GLD,
    )

    @staticmethod
    def check_quality_control_status(payload: XmlParser) -> list:
        faulty_statuses = []
        measurements = payload.get_list_of_elements_by_tag_name("TVPMeasurementMetadata") or []

        for m in measurements:
            qualifier = payload.get_child_element_by_tag_name(m, "qualifier")
            if qualifier is None:
                continue
            categories = payload.get_child_elements_by_tag_name(qualifier, "Category") or []
            for c in categories:
                codespace = payload.get_child_element_by_tag_name(c, "codeSpace")
                value = payload.get_child_element_by_tag_name(c, "value")
                if codespace is None or value is None:
                    continue
                if codespace.attrib.get(XLINKHREF) == "urn:bro:gld:StatusQualityControl" and value.text not in [
                    "goedgekeurd",
                    "nogNietBeoordeeld",
                ]:
                    faulty_statuses.append(value.text)

        return faulty_statuses

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        faulty_statuses = self.check_quality_control_status(payload)

        if faulty_statuses:
            feedback_message = self.rule_info.feedback_message % ", ".join(set(faulty_statuses))
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
