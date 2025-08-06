from app.domain.models.player import PlayerProfile, Inventory, Device, Clan
from app.ports.player_repository import PlayerProfileRepository
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel
from app.domain.exceptions import PlayerNotFoundError

class SqlAlchemyPlayerRepo(PlayerProfileRepository):
    def __init__(self, db_session_factory):
        self.db_session_factory = db_session_factory

    def get_by_id(self, player_id: str) -> PlayerProfile:
        with self.db_session_factory() as session:
            db_player = session.query(PlayerProfileDBModel).filter_by(player_id=player_id).first()
            if not db_player:
                raise PlayerNotFoundError()

            return PlayerProfile(
                player_id=db_player.player_id,
                credential=db_player.credential,
                created=db_player.created,
                modified=db_player.modified,
                last_session=db_player.last_session,
                total_spent=db_player.total_spent,
                total_refund=db_player.total_refund,
                total_transactions=db_player.total_transactions,
                last_purchase=db_player.last_purchase,
                active_campaigns=db_player.active_campaigns or [],
                devices=[Device(**d) for d in db_player.devices],
                level=db_player.level,
                xp=db_player.xp,
                total_playtime=db_player.total_playtime,
                country=db_player.country,
                language=db_player.language,
                birth_date=db_player.birth_date,
                gender=db_player.gender,
                inventory=Inventory(**db_player.inventory),
                clan=Clan(**db_player.clan) if db_player.clan else None,
                custom_field=db_player.custom_field,
            )

    def save(self, profile: PlayerProfile) -> None:
        with self.db_session_factory() as session:
            db_player = session.query(PlayerProfileDBModel).filter_by(player_id=profile.player_id).first()
            if not db_player:
                raise PlayerNotFoundError()

            db_player.modified = profile.modified
            db_player.active_campaigns = profile.active_campaigns
            db_player.devices = [device.model_dump() for device in profile.devices]
            db_player.inventory = profile.inventory.model_dump()
            db_player.clan = profile.clan.model_dump() if profile.clan else None
            db_player.custom_field = profile.custom_field

            session.commit()