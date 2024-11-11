from abc import ABC, abstractmethod
from typing import Generic, TypeVarTuple, Unpack

from app.schemas import RuleInfo, RuleResult

Parsers = TypeVarTuple("Parsers")


class BaseRule(ABC, Generic[*Parsers]):
    rule_info: RuleInfo

    def __init__(self):
        if not getattr(self, "rule_info", None):
            raise NotImplementedError("The rule_info attribute is not defined")
        if not isinstance(self.rule_info, RuleInfo):
            raise TypeError(f"rule_info is not of type {type(RuleInfo)}")

    @abstractmethod
    def apply_rule(self, *payload: Unpack[Parsers]) -> RuleResult:
        """
        :param payload: The original request payload submitted by the user.
        """
        ...

    def get_feedback_message(self):
        """
        Get the feedback message for the rule.
        Can be overridden by subclasses if custom formatting is needed.
        """
        return self.rule_info.feedback_message

    def assert_result(self, result: RuleResult):
        """
        Assert the result and print feedback message if the assertion fails.
        """
        if not result.passed:
            print(result.feedback_message)
            assert not result.passed
        else:
            assert result.passed
