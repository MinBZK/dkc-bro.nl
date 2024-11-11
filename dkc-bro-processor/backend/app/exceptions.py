from typing import Type


class RuleNotFound(Exception):
    def __init__(self, rule_code: str):
        super().__init__(f"Rule '{rule_code}' was not found in the rule registry")


class UnsupportedPayloadType(Exception):
    def __init__(self, rule_code: str, payload_type: Type):
        super().__init__(f"Rule '{rule_code}' does not support payloads of type '{payload_type.__name__}'")


class InvalidRuleParams(Exception):
    def __init__(self, rule_code: str):
        super().__init__(f"Rule '{rule_code}' was provided with invalid parameters")
