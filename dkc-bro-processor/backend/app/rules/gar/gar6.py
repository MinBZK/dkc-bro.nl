from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GAR6(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GAR6 controleert of alle gebruikte normen en standaarden bekend zijn en geschikt voor RWS.
        Normen en standaarden die worden gecontroleerd op waarde RWS zijn: (qualityControlMethod, analyticalTechnique, valuationMethod).

        Document is in overtreding wanneer een van de normen onbekend is of niet RWS waardes bevat.
        """,
        feedback_message="%s",
        explanation="""
        Controleert of er gewerkt is met bekende normen en standaarden. (qualityControlMethod, analyticalTechnique,
        valuationMethod)
        """,
        code="06",
        name="Normen en standaarden",
        object_type=ObjectType.GAR,
    )

    @staticmethod
    def check_norms_and_standards(payload: XmlParser) -> str:
        quality_control_method = payload.get_element_from_metadata("qualityControlMethod")
        valuation_methods = payload.get_list_of_elements_by_tag_name("valuationMethod")

        if quality_control_method is None:
            return "Gebruikte normen en standaarden (qualityControlMethod) ontbreken."
        elif quality_control_method == "onbekend":
            return "Gebruikte normen en standaarden zijn ingevuld met de waarde: 'onbekend'."
        elif not valuation_methods:
            return "Gebruikte normen en standaarden (valuationMethod) ontbreken."
        elif not all(vm.text and vm.text.startswith("RWS") for vm in valuation_methods):
            non_rws_values = ", ".join(vm.text for vm in valuation_methods if not (vm.text and vm.text.startswith("RWS")))
            return f"Gebruikte normen en standaarden zijn niet geschikt voor RWS. De gevonden waardes zijn: {non_rws_values}."
        return ""

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        error_message = self.check_norms_and_standards(payload)

        if error_message:
            feedback_message = self.rule_info.feedback_message % error_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
