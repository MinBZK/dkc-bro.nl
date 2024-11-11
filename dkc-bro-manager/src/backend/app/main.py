from app.app_factory import create_app
from app.expert.expert_rws import ExpertRws

app = create_app(ExpertRws)
