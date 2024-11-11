from enum import StrEnum, auto
from typing import Any, Union, Self

from pydantic import BaseModel as PydanticModel
from pydantic import Field, model_validator


class ObjectType(StrEnum):
    GEN = "GEN"
    BHR_GT = "BHR-GT"
    CPT = "CPT"
    GAR = "GAR"
    GLD = "GLD"
    GMW = "GMW"


class SeverityLevel(StrEnum):
    INFO = auto()
    WARNING = auto()
    ERROR = auto()


class RuleInfo(PydanticModel):
    docstring: str
    feedback_message: str
    explanation: str
    code: str
    name: str
    object_type: ObjectType

    @model_validator(mode="before")
    @classmethod
    def strip_whitespace(cls, data: Self) -> Self:
        """
        For every string field, strip leading and trailing whitespace. The return type must be the same as the input type.
        """
        return {
            key: value.strip().replace("\n", " ")
            if isinstance(value, str) else value
            for key, value in data.items()
        }


class RuleResult(PydanticModel):
    feedback_message: str | None = Field(..., description="A message to convey")
    passed: bool | None = Field(
        None,
        description="Indicates whether the validation passed or failed.",
    )

    @model_validator(mode="after")
    def check_passed_or_result(cls, values):
        if values.passed is None and values.result is None:
            raise ValueError("Either 'passed' or 'result' must be set.")
        return values


json_serializable = Union[str, list[Any], dict[str, Any]]


class RuleApplicationRequest(PydanticModel):
    rule_code: str = Field(
        ...,
        description="The code of the rule to apply.",
    )
    payload: bytes = Field(
        ...,
        description="The payload to apply the rule to.",
    )

    # Displayed in the OpenAPI documentation
    class ConfigDict:
        json_schema_extra = {
            "examples": [
                {
                    "rule_code": "GEN0001",
                    "payload": (
                        "Uit de statistieken van het CBS is niet af te leiden of "
                        "de totstandkoming van quantummechanische tunneling ook te maken heeft "
                        "met de semantische eigenschappen van deeltjes die tunnelen."
                    ),
                }
            ]
        }
