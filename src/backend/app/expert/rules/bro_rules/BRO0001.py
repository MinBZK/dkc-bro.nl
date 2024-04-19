# Imports from generic component
import re
from typing import List

import app.enums as enums
from app.expert.rules._superrule import superRule


class BRO0001(superRule):
    __docstring = """
    Controleregel BRO0001 controleert of het veld Object-id bronhouder (objectIdAccountableParty) voldoet aan het format afgesproken met RWS.
    Het objectIdAccountableParty wordt door middel van XML-parsing uit het brondocument gelezen en tegen een Reguliere Expressie aangehouden die de geldigheid controleert.
    De Reguliere Expressie test op de aanwezigheid en vorm van de elementen: WBS-SAP nummer, Zaaknummer RWS, Referentie RWS en Referentie ONG, waarbij Referentie ONG optioneel is.
    De elementen dienen individueel aan het format te voldoen en aan elkaar verbonden te zijn met streepjes -.
    Voorbeeld van een geldig Object-id bronhouder: P.00000183.0002-12345678-A15-15.2xx-F-11-ongreference

    Document is in overtreding wanneer objectIdAccountableParty niet voldoet aan het geëiste formaat.
    """
    __feedbackMessage = "Object-id bronhouder (objectIdAccountableParty) voldoet niet aan het afgesproken format."
    __explanation = "Controleert of het Object-id bronhouder (objectIdAccountableParty) voldoet aan het format zoals gevraagd door RWS."
    code = 1
    name = "Object-id bronhouder"
    object_type = "BRO"

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

    def check_object_id_accountable_party(self, object_id: str) -> List[str]:
        pattern = (
            "^"
            "(\[?[a-zA-Z]\.\d{8}\.\d{4}\]?)-"  # WBS-SAP
            "(\[?\d{8}\]?)-"  # Zaaknummer RWS
            "(\[?.+\]?)"  # Referentie RWS (vrije invoerveld)
            "(-.+)?"  # Referentie ONG (vrije invoerveld)
            "$"
        )
        regex = re.compile(pattern)
        return bool(regex.match(object_id))

    def applyRule(self, doc):
        object_id = doc.get_element_from_metadata("objectIdAccountableParty")
        return (
            self.getFeedbackMessage()
            if not object_id or not self.check_object_id_accountable_party(object_id)
            else None
        )
