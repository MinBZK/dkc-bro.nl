from fastapi import APIRouter

router = APIRouter()


@router.get("", include_in_schema=False)
async def healthcheck() -> dict[str, str]:
    """
    Execute a dummy query to check whether app still responds
    """
    return {"status": "OK"}
