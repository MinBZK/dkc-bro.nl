from app.parsers.xml_parser import XmlParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class GMW8(BaseRule[XmlParser]):
    supported_payload_types = [XmlParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel GMW8 controleert of alle peilbuizen bestaan uit materialen geschikt voor het doen van kwaliteitsmetingen.
        Om dit te controleren wordt gekeken naar de velden initialFunction, tubeMaterial, glue en de vulling hiervan.
        Als de initialFunction kwaliteit of kwaliteitStand is moet er lijm aanwezig zijn in de peilbuis.
        Daarnaast mag het materiaal van de buis dan niet voorkomen in "peHighDensity", "pvc" of "teflon".

        Document is in overtreding wanneer niet alle peilbuizen bestaan uit de juiste materialen volgens bovenstaande regels.
        """,
        feedback_message="%s",
        explanation="Deze regel controleert of de gebruikte materialen voldoen aan de eisen voor kwaliteitsmetingen indien van toepassing.",
        code="08",
        name="Gebruikte materialen buis",
        object_type=ObjectType.GMW,
    )

    @staticmethod
    def check_tube_materials(payload: XmlParser):
        initial_function = payload.get_element_by_tag_name("initialFunction").text  # pyright: ignore
        monitoring_tubes = payload.get_list_of_elements_by_tag_name("monitoringTube")
        invalid_tubes = []

        for index, monitoring_tube in enumerate(monitoring_tubes, start=1):  # pyright: ignore
            glue = payload.get_child_element_by_tag_name(monitoring_tube, "glue").text  # pyright: ignore
            tube_material = payload.get_child_element_by_tag_name(monitoring_tube, "tubeMaterial").text  # pyright: ignore
            if tube_material in ["peHighDensity", "pvc", "teflon"] or (
                glue in ["ongespecificeerd", "geen", "onbekend"] and initial_function in ["kwaliteit", "kwaliteitStand"]
            ):
                invalid_tubes.append((index, glue, tube_material))

        specific_messages = []
        ids_with_both_issues = []
        ids_with_wrong_material = []
        ids_with_no_glue = []

        for index, glue, tube_material in invalid_tubes:
            if initial_function in ["kwaliteit", "kwaliteitStand"]:
                if tube_material in ["peHighDensity", "pvc", "teflon"] and glue in ["ongespecificeerd", "geen", "onbekend"]:
                    ids_with_both_issues.append((index, glue, tube_material))
                elif tube_material in ["peHighDensity", "pvc", "teflon"]:
                    ids_with_wrong_material.append((index, tube_material))
                elif glue in ["ongespecificeerd", "geen", "onbekend"]:
                    ids_with_no_glue.append((index, glue))
            else:
                if tube_material in ["peHighDensity", "pvc", "teflon"]:
                    ids_with_wrong_material.append((index, tube_material))

        if ids_with_both_issues:
            specific_messages.append(
                "Peilbuis met ID: '%s' heeft geen lijm aanwezig: '%s', noch de juiste materialen voor kwaliteitsmetingen: '%s'."
                % (
                    ", ".join(str(tube_id) for tube_id, _, _ in ids_with_both_issues),
                    ", ".join(glue for _, glue, _ in ids_with_both_issues),
                    ", ".join(tube_material for _, _, tube_material in ids_with_both_issues),
                )
            )

        if ids_with_wrong_material:  # and not ids_with_both_issues:
            specific_messages.append(
                "Peilbuis met ID: '%s' gebruikt niet de juiste materialen voor kwaliteitsmetingen. De gevonden waarde is: '%s'."
                % (
                    ", ".join(str(tube_id) for tube_id, _ in ids_with_wrong_material),
                    ", ".join(tube_material for _, tube_material in ids_with_wrong_material),
                )
            )

        if ids_with_no_glue:  # and not ids_with_both_issues:
            specific_messages.append(
                "Peilbuis met ID: '%s' heeft geen garantie aanwezigheid lijm. De gevonden waarde is: '%s'."
                % (", ".join(str(tube_id) for tube_id, _ in ids_with_no_glue), ", ".join(glue for _, glue in ids_with_no_glue))
            )

        return " ".join(specific_messages) if specific_messages else None

    def apply_rule(self, payload: XmlParser) -> RuleResult:
        error_message = self.check_tube_materials(payload)

        if error_message:
            feedback_message = self.rule_info.feedback_message % error_message
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)
