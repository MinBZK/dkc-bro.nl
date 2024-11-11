# Import all the SQL Alchemy models so that Base has them before being imported by Alembic
from app.database.base_class import Base  # noqa
from app.models.batch import Batch  # noqa
from app.models.finding import Finding  # noqa
from app.models.rule import Rule  # noqa
from app.models.user import User  # noqa
