import logging

from fastapi import APIRouter, File, Form, HTTPException, UploadFile, status

from app import exceptions, rule_manager, schemas
from app.parsers.bhrgt_parser import BHRGTParser
from app.parsers.cpt_parser import CPTParser
from app.parsers.gar_parser import GARParser
from app.parsers.gld_parser import GLDParser
from app.parsers.gmw_parser import GMWParser

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/")
async def get_rule_info() -> list[schemas.RuleInfo]:
    """
    Get all available rules and their default information.
    """
    return rule_manager.get_all_rule_info()


@router.post("/apply")
async def apply_rule(payload: UploadFile = File(...), rule_code: str = Form(...)) -> schemas.RuleResult:
    """
    Apply the requested rule to the given XML file.
    """
    parsers = [BHRGTParser, CPTParser, GARParser, GLDParser, GMWParser]
    try:
        contents = await payload.read()
        object_type = rule_code[:3] if rule_code[:3] != "BHR" else "BHR-GT"

        if object_type == "GEN":
            parser = parsers[0].from_string(contents)
        else:
            valid_parsers = [parser for parser in parsers if parser.OBJECT_TYPE == object_type]
            parser = valid_parsers[0].from_string(contents)

        result = rule_manager.apply_rule(rule_code, parser)
        logger.info(f"Applied rule {rule_code} to XML file successfully.")
        return result

    except exceptions.RuleNotFound as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(e))

    except exceptions.UnsupportedPayloadType as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))

    except exceptions.InvalidRuleParams as e:
        logger.exception(e)
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(e))

    except Exception as e:
        logger.exception(e)
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "An unknown error occurred. Contact the developers for more details.",
        )
