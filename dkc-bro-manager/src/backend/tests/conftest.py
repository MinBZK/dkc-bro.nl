import pytest

from app.expert.expert_rws import ExpertRws
from app.expert.rules._superrule import superRule


# autouse fixture that mocks the expert_rws.__register_rules method
# and returns a list of superRule objects
@pytest.fixture(scope="session", autouse=True)
def mock_rule_registration(session_mocker):
    dummy_rules = [
        superRule(
            code="code",
            name="name",
            object_type="object_type",
            importance=1,
            feedbackMessage="feedback_message",
            explanation="explanation",
            docstring="docstring",
        )
    ]
    session_mocker.patch.object(
        ExpertRws, "_ExpertRws__register_rules", return_value=dummy_rules
    )
