from typing import Dict, List


def construct_summary_string(errors: int, warnings: int) -> str:
    """
    Given an error and warning count for a batch, construct the correct summary.

    Returns: Summary text.
    """
    message = "Deze levering heeft na controle "
    if errors + warnings <= 0:
        message += "geen bijzonderheden"
    if errors == 1:
        message += "1 fout"
    elif errors > 1:
        message += f"{errors} fouten"
    if errors > 0 and warnings > 0:
        message += " en "
    if warnings == 1:
        message += "1 waarschuwing"
    elif warnings > 1:
        message += f"{warnings} waarschuwingen"
    message += "."
    return message


def count_importance_occurrence_in_violations(
    rules: Dict, violations: List, importance: int
):
    """
    Counts the amount of findings with a given importance from a list of findings.

    Returns: Finding count with that level.
    """
    return len(
        [
            v
            for v in violations
            if rules[v.get("objectType") + "-" + str(v.get("ruleId"))].importance
            == importance
        ]
    )


def count_errors_in_violations(rules: Dict, violations: List):
    """
    Given a list of violations, return the amount of findings with error level.

    Returns: Number of errors in violations list
    """
    return count_importance_occurrence_in_violations(rules, violations, 3)


def count_warnings_in_violations(rules: Dict, violations: List):
    """
    Given a list of violations, return the amount of findings with warning level.

    Returns: Number of warnings in violations list
    """
    return count_importance_occurrence_in_violations(rules, violations, 2)
