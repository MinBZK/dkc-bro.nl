# Imports from generic component
import app.enums as enums
from app.expert.rules._superrule import superRule


class GMW0008(superRule):
    __docstring = """
    Controleregel GMW0008 controleert of alle peilbuizen bestaan uit materialen geschikt voor het doen van kwaliteitsmetingen.
    Om dit te controleren wordt gekeken naar de velden initialFunction, tubeMaterial, glue en de vulling hiervan.
    Als de initialFunction kwaliteit of kwaliteitStand is moet er lijm aanwezig zijn in de peilbuis.
    Daarnaast mag het materiaal van de buis dan niet voorkomen in "peHighDensity", "pvc" of "teflon".

    Document is in overtreding wanneer niet alle peilbuizen bestaan uit de juiste materialen volgens bovenstaande regels.
    """

    __feedbackMessage = "%s"
    __explanation = "Deze regel controleert of de gebruikte materialen voldoen aan de eisen voor kwaliteitsmetingen indien van toepassing."
    code = "08"
    name = "Gebruikte materialen buis"
    object_type = "GMW"

    def __init__(self, emergence=enums.Importance.ERROR):
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
        # validate materials
        initial_function = doc.get_element_by_tag_name("initialFunction").text
        monitoring_tubes = doc.get_list_of_elements_by_tag_name("monitoringTube")
        invalid_tubes = []

        for index, monitoring_tube in enumerate(monitoring_tubes, start=1):
            glue = doc.get_child_element_by_tag_name(monitoring_tube, "glue").text
            tube_material = doc.get_child_element_by_tag_name(
                monitoring_tube, "tubeMaterial"
            ).text
            has_wrong_material = tube_material in ["peHighDensity", "pvc", "teflon"]
            has_no_glue = glue in ["ongespecificeerd", "geen", "onbekend"]
            has_initial_function = initial_function in ["kwaliteit", "kwaliteitStand"]

            if has_wrong_material or (has_initial_function and has_no_glue):
                invalid_tubes.append(
                    (index, glue, tube_material, has_wrong_material, has_no_glue)
                )

        specific_messages = []
        ids_with_both_issues = []
        ids_with_wrong_material = []
        ids_with_no_glue = []

        for (
            index,
            glue,
            tube_material,
            has_wrong_material,
            has_no_glue,
        ) in invalid_tubes:
            if has_wrong_material and has_no_glue:
                ids_with_both_issues.append((index, glue, tube_material))
            elif has_wrong_material:
                ids_with_wrong_material.append((index, tube_material))
            elif has_no_glue:
                ids_with_no_glue.append((index, glue))

        if ids_with_both_issues:
            specific_messages.append(
                "Peilbuis met ID: '%s' heeft geen lijm aanwezig: '%s', noch de juiste materialen voor kwaliteitsmetingen: '%s'."
                % (
                    ", ".join(str(id) for id, _, _ in ids_with_both_issues),
                    ", ".join(glue for _, glue, _ in ids_with_both_issues),
                    ", ".join(
                        tube_material for _, _, tube_material in ids_with_both_issues
                    ),
                )
            )

        if ids_with_wrong_material:
            specific_messages.append(
                "Peilbuis met ID: '%s' gebruikt niet de juiste materialen voor kwaliteitsmetingen. De gevonden waarde is: '%s'."
                % (
                    ", ".join(str(id) for id, _ in ids_with_wrong_material),
                    ", ".join(
                        tube_material for _, tube_material in ids_with_wrong_material
                    ),
                )
            )

        if ids_with_no_glue:
            specific_messages.append(
                "Peilbuis met ID: '%s' heeft geen garantie aanwezigheid lijm. De gevonden waarde is: '%s'."
                % (
                    ", ".join(str(id) for id, _ in ids_with_no_glue),
                    ", ".join(glue for _, glue in ids_with_no_glue),
                )
            )

        error_message = " ".join(specific_messages) if specific_messages else None

        if error_message:
            return self.getFeedbackMessage() % error_message
        else:
            return None
