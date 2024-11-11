import importlib
import logging
import os
from typing import Dict, List, Optional, Type, TypeVarTuple, Unpack

from app.exceptions import RuleNotFound
from app.rules import BaseRule
from app.schemas import RuleInfo, RuleResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Parsers = TypeVarTuple("Parsers")

# Constants
RULES_DIR = "rules"
RULE_FILE_SUFFIX = ".py"


class RuleRegistry:
    """A registry for managing and accessing rule classes."""

    def __init__(self):
        self._rules: Dict[str, Type[BaseRule]] = {}

    def register(self, rule_code: str, rule_class: Type[BaseRule]) -> None:
        """Register a rule class with the given code."""
        self._rules[rule_code] = rule_class

    def get(self, rule_code: str) -> Optional[Type[BaseRule]]:
        """Retrieve a rule class by its code."""
        return self._rules.get(rule_code)

    def get_all(self) -> Dict[str, Type[BaseRule]]:
        """Get all registered rules."""
        return self._rules.copy()

    def __len__(self) -> int:
        return len(self._rules)


rule_registry = RuleRegistry()


def import_rules(rules_path: str) -> None:
    """
    Import all rule classes from the specified directory.

    Args:
        rules_path (str): Path to the directory containing rule modules.
    """

    def get_rule_modules(path: str) -> List[str]:
        return [
            f"app.{RULES_DIR}.{subdir}.{file[:-len(RULE_FILE_SUFFIX)]}"
            for subdir in os.listdir(path)
            if os.path.isdir(os.path.join(path, subdir)) and not subdir.startswith("__")
            for file in os.listdir(os.path.join(path, subdir))
            if file.endswith(RULE_FILE_SUFFIX) and not file.startswith("__")
        ]

    logging.info(get_rule_modules(rules_path))
    for module_name in get_rule_modules(rules_path):
        try:
            module = importlib.import_module(module_name)
            rule_class = next(
                obj for _, obj in module.__dict__.items() if isinstance(obj, type) and issubclass(obj, BaseRule) and obj != BaseRule
            )
            rule_code = f"{rule_class.rule_info.object_type.replace("_", "-").upper()}{rule_class.rule_info.code}"
            rule_registry.register(rule_code, rule_class)
            logger.info(f"Registered rule: {rule_code}")
        except (ImportError, StopIteration) as e:
            logger.error(f"Error processing {module_name}: {e}")

    logger.info(f"Total rules registered: {len(rule_registry)}")


def get_all_rule_info() -> List[RuleInfo]:
    """
    Get information about all registered rules.

    Returns:
        List[RuleInfo]: A list of RuleInfo objects for all registered rules.
    """
    return [RuleInfo(**rule.rule_info.model_dump()) for rule in rule_registry.get_all().values()]


def get_rule_class(rule_code: str) -> Type[BaseRule]:
    """
    Get the rule class for a given rule code.

    Args:
        rule_code (str): The code of the rule to retrieve.

    Returns:
        Type[BaseRule]: The rule class.

    Raises:
        RuleNotFound: If no rule is found for the given code.
    """
    rule_class = rule_registry.get(rule_code)
    if rule_class is None:
        raise RuleNotFound(rule_code)
    return rule_class


def apply_rule(rule_code: str, *payload: Unpack[Parsers]) -> RuleResult:
    """
    Apply a rule to the given payload.

    Args:
        rule_code (str): The code of the rule to apply.
        *payload: The payload to apply the rule to.

    Returns:
        RuleResult: The result of applying the rule.

    Raises:
        RuleNotFound: If no rule is found for the given code.
        UnsupportedPayloadType: If the payload type is not supported by the rule.
    """
    rule_class = get_rule_class(rule_code)
    return rule_class().apply_rule(payload[0])


# Import rules when this module is loaded
current_dir = os.path.dirname(__file__)
rules_dir = os.path.join(current_dir, RULES_DIR)
import_rules(rules_dir)
