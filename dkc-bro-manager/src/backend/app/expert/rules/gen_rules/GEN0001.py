# Imports from generic component
import re
from typing import List

import app.enums as enums
from app.expert.rules._superrule import superRule


class GEN0001(superRule):
    __docstring = """
    Controleregel GEN0001 controleert of het veld Object-id bronhouder (objectIdAccountableParty) voldoet aan het format afgesproken met RWS. Deze format is als volgt:
    [WBS-nummer X.xxxxxxxx.xxxx]-[zaaknummer RWS xxxxxxxx]-[specificatie RWS]-[referentie ON], voorbeeld: [P.00000183.0002]-[31168417]-[A15-15.2xx-S-05]-[referentie ON].
    Het objectIdAccountableParty wordt door middel van XML-parsing uit het brondocument gelezen en tegen een Reguliere Expressie aangehouden die de geldigheid controleert.
    """
    __feedbackMessage = "Object-id bronhouder (objectIdAccountableParty) voldoet niet aan het afgesproken format. De werkelijke object-id uit de xml is %s"
    __explanation = "Controleert of het Object-id bronhouder (objectIdAccountableParty) voldoet aan het format zoals gevraagd door RWS."
    code = "01"
    name = "Object-id bronhouder"
    object_type = "GEN"

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
            "(\[?[a-zA-Z]\.\d{6}(?:\d{2})?\.?\d{0,4}\]?)-(\[?\d{8}]?(?:-.*?)?\]?)$"
        )
        regex = re.compile(pattern)
        return bool(regex.match(object_id))

    def applyRule(self, doc):
        object_id = doc.get_element_from_metadata("objectIdAccountableParty")
        print(object_id)
        return (
            self.getFeedbackMessage() % (object_id)
            if not object_id or not self.check_object_id_accountable_party(object_id)
            else None
        )
