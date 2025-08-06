from sqlalchemy.orm import Session
from app.ports.player_repository import PlayerProfileRepository
from app.domain.models.player import PlayerProfile
from app.domain.exceptions import PlayerNotFoundError
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel

class SqlAlchemyPlayerRepo(PlayerProfileRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def get_by_id(self, player_id: str) -> PlayerProfile:
        row = self.db.query(PlayerProfileDBModel).filter_by(player_id=player_id).first()
        if not row:
            raise PlayerNotFoundError()
        return PlayerProfile.model_validate(row.__dict__)

    def save(self, profile: PlayerProfile) -> None:
        db_model = PlayerProfileDBModel(**profile.model_dump())
        self.db.merge(db_model)
        self.db.commit()