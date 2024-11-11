from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult
from app.utils.parser_utils import XLINKHREF


class GLD7(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GLD7 controleert of de beoordelingsprocedure voor alle aangeboden metingen volgens het QC-Protocol
        (PMBProtocolDatakwaliteitscontroleQC2018v2.0) is. Om dit te controleren worden de velden ObservationProcess, parameter,
        named value, name, value gebruikt.

        Document is in overtreding wanneer de beoordelingsprocedure niet voor alle metingen gelijk is aan QC-Protocol
        (PMBProtocolDatakwaliteitscontroleQC2018v2.0).
        """,
        feedback_message="""
        Gebruikte beoordelingsprocedure is niet volgens het QC-Protocol voor meting(en) met ID: '%s'. De gevonden waarde
        is: '%s'.
        """,
        explanation="Controleert of de kwaliteitsborging van alle metingen is gedaan volgens het QC-Protocol.",
        code="07",
        name="Beoordelingsprocedure",
        object_type=ObjectType.GLD,
    )

    @staticmethod
    def check_evaluation_procedure(payload: XmlParser) -> list:
        observation_processes = payload.get_list_of_elements_by_tag_name("ObservationProcess") or []
        violated_instances = []

        for index, op in enumerate(observation_processes, start=1):
            parameters = payload.get_child_elements_by_tag_name(op, "parameter") or []
            for p in parameters:
                named_value = payload.get_child_element_by_tag_name(p, "NamedValue")
                if named_value is None:
                    continue
                name = payload.get_child_element_by_tag_name(named_value, "name")
                value = payload.get_child_element_by_tag_name(named_value, "value")
                if name is None or value is None:
                    continue
                if (
                    name.attrib.get(XLINKHREF) == "urn:bro:gld:ObservationProcess:evaluationProcedure"
                    and value.text != "PMBProtocolDatakwaliteitscontroleQC2018v2.0"
                ):
                    violated_instances.append((index, value.text))

        return violated_instances

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        violated_instances = self.check_evaluation_procedure(payload)

        if violated_instances:
            indices, values = zip(*violated_instances)
            feedback_message = self.rule_info.feedback_message % (
                ", ".join(map(str, indices)),
                ", ".join(values),
            )
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
