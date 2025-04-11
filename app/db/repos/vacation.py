from sqlalchemy.orm import Session
from models.vacation import Vacation

class VacationRepository:
    def __init__(self, session: Session):
        self.session = session

    # def create(self, data: VacationInput):

    # def get_all(self) -> List[UserOutput]:
    #     users = self.session.query(Vacation).all()
    #     return users
    