# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GAR0006(superRule):
    __docstring = """
    Controleregel GAR0006 controleert of alle gebruikte normen en standaarden bekend zijn en geschikt voor RWS.
    Normen en standaarden die worden gecontroleerd op waarde RWS zijn: (qualityControlMethod, analyticalTechnique, valuationMethod).

    Document is in overtreding wanneer een van de normen onbekend is of niet RWS waardes bevat.
    """

    __feedbackMessage = "%s"
    __explanation = "Controleert of er gewerkt is met bekende normen en standaarden. (qualityControlMethod, analyticalTechnique, valuationMethod)"
    code = "06"
    name = "Normen en standaarden"
    object_type = "GAR"

    def __init__(self, emergence=enums.Importance.INFO):
        super().__init__(
            self.code,
            self.name,
            self.object_type,
            emergence,
            self.__feedbackMessage,
            self.__explanation,
            self.__docstring,
        )

    def applyRule(self, doc):
        ## TODO:: Check if there is a possibility that we have more instances of the same tag in a single xml file (if so, we need to use IDs) - like GLD0006
        quality_control_method = doc.get_element_from_metadata("qualityControlMethod")
        valuation_methods = doc.get_list_of_elements_by_tag_name("valuationMethod")

        if quality_control_method == "onbekend":
            specific_message = f"Gebruikte normen en standaarden zijn ingevuld met de waarde: '{quality_control_method}'."
            return self.getFeedbackMessage() % specific_message
        elif not all([vm.text.startswith("RWS") for vm in valuation_methods]):
            specific_message = f"Gebruikte normen en standaarden zijn niet geschikt voor RWS. De gevonden waardes zijn: {', '.join([vm.text for vm in valuation_methods])}."
            return self.getFeedbackMessage() % specific_message
        else:
            return None
