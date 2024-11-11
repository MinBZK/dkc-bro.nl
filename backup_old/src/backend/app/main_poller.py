from fastapi_utils.tasks import repeat_every

# Imports from generic component
from app.app_factory import create_app
from app.expert.expert_rws import ExpertRws
from app.levering_handler.levering_handler import LeveringHandler

app = create_app(ExpertRws)


@app.on_event("startup")
@repeat_every(seconds=15)
async def bhp_poller() -> None:
    handler = LeveringHandler()
    handler.poll_and_handle_leveringen()
