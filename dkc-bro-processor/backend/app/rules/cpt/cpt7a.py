from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT7A(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT7A controleert of het Domein Kwaliteitsklasse (qualityClass) is gevuld met een geldige waarde.
        De regel bevat een lijst van niet-geldige waarden waar tegen de waarde uit het document wordt vergeleken.
        De lijst bevat de waardes klasse 4 en alles lager dan klasse 4.

        Document is in overtreding wanneer Domein Kwaliteitsklasse (qualityClass) is gevuld met een waarde uit de lijst niet geldige
        kwaliteitsklassen.
        """,
        feedback_message="Domein Kwaliteitsklasse (qualityClass) is gevuld met een niet geldige waarde: '%s'.",
        explanation="""
        Controleert of het Domein Kwaliteitsklasse (qualityClass) gevuld is met klasse4 of lager. Indien dit het geval is moet
        het object gerouterneerd worden.
        """,
        code="07A",
        name="Domein Kwaliteitsklasse (BRO)",
        object_type=ObjectType.CPT,
    )

    invalid_quality_classes = [
        "klasse4",
        "klasse5",
        "klasse6",
        "klasse7",
        "nvt",
        "onbekend",
    ]

    @staticmethod
    def check_quality_class(payload: CPTParser):
        return payload.get_element_from_metadata("qualityClass")

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        quality_class = self.check_quality_class(payload)
        if quality_class in self.invalid_quality_classes:
            feedback_message = self.rule_info.feedback_message % quality_class
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
