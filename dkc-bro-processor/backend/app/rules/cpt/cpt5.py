from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT5(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT5 controleert of het domein Stopcriterium correct is ingevuld. De regel bevat een lijst van valide stop criteria en
        legt het veld Domein Stopcriterium (stopCriterion) hier tegen aan.

        Document is in overtreding wanneer Domein Stopcriterium (stopCriterion) niet aanwezig is in de lijst van valide stopcriteria.
        """,
        feedback_message="%s",
        explanation="""
        Controleert of het Domein Stopcriterium (stopCriterion) gevuld is met een geldige waarde uit de codelijst die niet
        gelijk is aan onbekend.
        """,
        code="05",
        name="Domein Stopcriterium (BRO)",
        object_type=ObjectType.CPT,
    )

    valid_stop_criterions = [
        "bezwijkrisico",
        "conusweerstand",
        "einddiepte",
        "hellingshoek",
        "obstakel",
        "storing",
        "waterspanning",
        "wegdrukkracht",
        "wrijvingsweerstand",
    ]

    @staticmethod
    def check_stop_criterion(payload: CPTParser) -> str:
        stop_criterion = payload.get_element_from_metadata("stopCriterion")

        if stop_criterion == "onbekend":
            return f"Domein Stopcriterium (stopCriterion) is met een waarde ingevuld met de waarde: '{stop_criterion}'."
        elif stop_criterion not in CPT5.valid_stop_criterions:
            return f"Domein Stopcriterium (stopCriterion) is ingevuld met een waarde die niet op de codelijst staat: '{stop_criterion}'."
        return ""

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        error_message = self.check_stop_criterion(payload)

        if error_message:
            feedback_message = self.rule_info.feedback_message % error_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
