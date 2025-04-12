from . import engine
from .models import Deps, VacationRequest, Employee


def create_tables():
    Deps.metadata.create_all(bind=engine, checkfirst=True)
    VacationRequest.metadata.create_all(bind=engine, checkfirst=True)
    Employee.metadata.create_all(bind=engine, checkfirst=True)