from app.levering_handler.utils import (construct_summary_string,
                                        count_errors_in_violations,
                                        count_warnings_in_violations)
from app.schemas.rule import Rule


def test_construct_summary_string():
    """
    Tests the correct construction of summary strings sent to BHP for given error and warning counts.
    """
    assert (
        construct_summary_string(0, 0)
        == "Deze levering heeft na controle geen bijzonderheden."
    )
    assert construct_summary_string(1, 0) == "Deze levering heeft na controle 1 fout."
    assert construct_summary_string(2, 0) == "Deze levering heeft na controle 2 fouten."
    assert (
        construct_summary_string(0, 1)
        == "Deze levering heeft na controle 1 waarschuwing."
    )
    assert (
        construct_summary_string(0, 2)
        == "Deze levering heeft na controle 2 waarschuwingen."
    )
    assert (
        construct_summary_string(1, 1)
        == "Deze levering heeft na controle 1 fout en 1 waarschuwing."
    )
    assert (
        construct_summary_string(1, 2)
        == "Deze levering heeft na controle 1 fout en 2 waarschuwingen."
    )
    assert (
        construct_summary_string(2, 1)
        == "Deze levering heeft na controle 2 fouten en 1 waarschuwing."
    )
    assert (
        construct_summary_string(2, 2)
        == "Deze levering heeft na controle 2 fouten en 2 waarschuwingen."
    )


def mock_rule_with_importance(importance: int):
    return Rule(
        name="mock",
        object_type="mock",
        importance=importance,
        explanation="mock explanation",
        docstring="mock docstring",
        ruleType=1,
        enabled=True,
        id=1,
    )


def test_count_errors_in_violations():
    mock_rules = {
        "mock-1": mock_rule_with_importance(3),
        "mock-2": mock_rule_with_importance(2),
        "mock-3": mock_rule_with_importance(3),
        "mock-4": mock_rule_with_importance(3),
        "mock-5": mock_rule_with_importance(1),
    }
    mock_violations = [
        {"objectType": "mock", "ruleId": 1},
        {"objectType": "mock", "ruleId": 2},
        {"objectType": "mock", "ruleId": 3},
        {"objectType": "mock", "ruleId": 3},
    ]
    assert count_errors_in_violations(mock_rules, mock_violations) == 3


def test_count_warnings_in_violations():
    mock_rules = {
        "mock-1": mock_rule_with_importance(2),
        "mock-2": mock_rule_with_importance(2),
        "mock-3": mock_rule_with_importance(3),
        "mock-4": mock_rule_with_importance(3),
        "mock-5": mock_rule_with_importance(1),
    }
    mock_violations = [
        {"objectType": "mock", "ruleId": 1},
        {"objectType": "mock", "ruleId": 2},
        {"objectType": "mock", "ruleId": 3},
        {"objectType": "mock", "ruleId": 3},
    ]
    assert count_warnings_in_violations(mock_rules, mock_violations) == 2
