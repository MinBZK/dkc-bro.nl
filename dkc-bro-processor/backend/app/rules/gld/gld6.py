from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult
from app.utils.parser_utils import XLINKHREF


class GLD6(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GLD6 controleert of de meetprocedure voor alle aangeboden metingen de RWS-meetprocedure (RWSgwmon) is.
        Om dit te controleren worden de velden ObservationProcess => processReference gebruikt.

        Document is in overtreding wanneer de meetprocedure niet voor alle metingen gelijk is aan (RWSgwmon).
        """,
        feedback_message="""
        Gebruikte meetprocedure is niet gelijk aan de RWS-meetprocedure (RWSgwmon) voor de meting(en) met ID: '%s'.
        De gevonden waarde is: '%s'.
        """,
        explanation="Controleert of de RWS-meetprocedure (RWSgwmon) is gebruikt voor de aangeboden metingen.",
        code="06",
        name="Meetprocedure",
        object_type=ObjectType.GLD,
    )

    @staticmethod
    def check_observation_processes(payload: XmlParser) -> list:
        faulty_procedures = []
        observation_processes = payload.get_list_of_elements_by_tag_name("ObservationProcess") or []

        for index, op in enumerate(observation_processes, start=1):
            reference = payload.get_child_element_by_tag_name(op, "processReference")
            if reference is None or XLINKHREF not in reference.attrib:
                continue
            href_value = reference.attrib[XLINKHREF]
            href_value = href_value.split(":")[-1]
            if not href_value.endswith("RWSgwmon"):
                faulty_procedures.append((index, href_value))

        return faulty_procedures

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        faulty_procedures = self.check_observation_processes(payload)

        if faulty_procedures:
            messages = []
            for index, href_value in faulty_procedures:
                messages.append(self.rule_info.feedback_message % (index, href_value))
            feedback_message = "\n".join(messages)
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
