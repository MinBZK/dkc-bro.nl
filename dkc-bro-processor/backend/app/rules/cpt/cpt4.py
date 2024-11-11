from typing import Tuple

import app.utils.enums as rws_enums
import app.utils.putils as putils
from app.parsers.cpt_parser import CPTParser
from app.rules.base_rule import BaseRule
from app.schemas import ObjectType, RuleInfo, RuleResult


class CPT4(BaseRule[CPTParser]):
    supported_payload_types = [CPTParser]
    rule_info = RuleInfo(
        docstring="""
        Controleregel CPT4 controleert of de Conuspenetratietest plaatselijke wrijving (localFriction) is ingevuld in iedere meetwaarde
        in de CPT. Wanneer deze niet in iedere meetwaarde is ingevuld, zal de controleregel bijhouden voor hoeveel meetwaarden dit niet is
        gedaan.

        Document is in overtreding wanneer Conuspenetratietest plaatselijke wrijving (localFriction) niet in iedere regel is ingevuld.
        """,
        feedback_message="""
        In de %s regels met meetwaarden is Conuspenetratietest plaatselijke wrijving (localFriction) %s keer niet
        ingevuld.""",
        explanation="Controleert hoeveel meetwaardes van de plaatselijke wrijving (localFriction) niet is ingevuld van een CPT",
        code="04",
        name="Plaatselijke wrijving",
        object_type=ObjectType.CPT,
    )

    @staticmethod
    def check_cpt_local_friction(payload: CPTParser) -> Tuple[int, int]:
        index, param_name = rws_enums.CPTParams.LOCALFRICTION.value
        if putils.cpt_parameters_filled(payload.get_cpt_parameters_map(), param_name):
            cpt_matrix = payload.get_cpt_matrix()
            if cpt_matrix is not None:
                total_rows = len(cpt_matrix)
                missing_local_frictions = sum(1 for row in cpt_matrix if row[index] == rws_enums.MISSINGVALUE)
                return total_rows, missing_local_frictions
        return 0, 0

    def apply_rule(self, payload: CPTParser) -> RuleResult:
        total_rows, missing_local_frictions = self.check_cpt_local_friction(payload)

        if missing_local_frictions > 0:
            feedback_message = self.rule_info.feedback_message % (
                total_rows,
                missing_local_frictions,
            )
            passed = False
        else:
            feedback_message = None
            passed = True

        return RuleResult(feedback_message=feedback_message, passed=passed)