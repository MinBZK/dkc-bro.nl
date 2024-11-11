import json
from abc import ABC
from json.decoder import JSONDecodeError
from typing import Any, Dict


class JsonDocumentParser(ABC):
    def __init__(self, raw_json: str):
        self.raw_json: str = raw_json
        self.data: Dict[str, Any] = {}
        self.valid_json: bool = False
        self.is_request_of_type: bool = False
        self.object_type: str = ""

        self._parse_json()

    def _parse_json(self) -> None:
        """Parse the raw JSON string and set the valid_json flag."""
        try:
            self.data = json.loads(self.raw_json)
            self.valid_json = True
        except JSONDecodeError as err:
            raise ValueError(f"Could not parse JSON input: {err}") from err

    @property
    def is_valid_json(self) -> bool:
        """Return whether the JSON is valid."""
        return self.valid_json

    @property
    def is_of_type(self) -> bool:
        """Return whether the document is of the expected type."""
        return self.is_request_of_type

    @property
    def get_object_type(self) -> str:
        """Return the object type."""
        return self.object_type

    def get_attribute(self, attr_name: str) -> Any:
        """
        Get the value of a specified attribute from the JSON data.

        Args:
            attr_name (str): The name of the attribute to retrieve.

        Returns:
            The value of the attribute.

        Raises:
            KeyError: If the attribute is not found in the JSON data.
        """
        try:
            return self.data[attr_name]
        except KeyError:
            raise KeyError(f"Attribute '{attr_name}' not found in JSON data")
