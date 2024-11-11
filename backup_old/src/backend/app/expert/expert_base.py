from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

from app.expert.rules._superrule import superRule


class ExpertBase(ABC):
    def __init__(self):
        self._rule_path: Path = None
        self._rules: List[superRule] = None
        self._parsers: List = None

    @property
    def rule_path(self) -> Path:
        """
        Getter for the experts known rule path.
        """
        return self._rule_path

    @rule_path.setter
    def rule_path(self, rule_path: Path) -> None:
        """
        Setter for the experts known rule path.
        """
        self._rule_path = rule_path

    @property
    def rules(self) -> List[superRule]:
        """
        Getter for the experts known rules.
        """
        return self._rules

    @rules.setter
    def rules(self, rules: List[superRule]) -> None:
        """
        Setter for the experts known rules.
        """
        self._rules = rules

    @property
    def parsers(self) -> List:
        """
        Getter for the experts known parsers.
        """
        return self._parsers

    @parsers.setter
    def parsers(self, parsers: List) -> None:
        """
        Setter for the experts known parsers.
        """
        self._parsers = parsers

    @abstractmethod
    def validate_documents(self, documents: List) -> List:
        """Validates a list of documents returning a list of findings."""
        raise NotImplementedError

    @abstractmethod
    def generate_report(self, batch_id: str, data, historicaldata=None) -> str:
        """generates a pdf report based on batch identifier and dataset"""
        raise NotImplementedError

    @abstractmethod
    def scan_and_validate_documents(self) -> None:
        """validates all documents located on a PVC"""
        raise NotImplementedError
