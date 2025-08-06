import json
from app.domain.models.player import PlayerProfile
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel

def domain_to_db_model(profile: PlayerProfile) -> PlayerProfileDBModel:
    return PlayerProfileDBModel(
        player_id=profile.player_id,
        credential=profile.credential,
        created=profile.created,
        modified=profile.modified,
        last_session=profile.last_session,
        total_spent=profile.total_spent,
        total_refund=profile.total_refund,
        total_transactions=profile.total_transactions,
        last_purchase=profile.last_purchase,
        active_campaigns=profile.active_campaigns,
        devices=[device.model_dump() for device in profile.devices],
        level=profile.level,
        xp=profile.xp,
        total_playtime=profile.total_playtime,
        country=profile.country,
        language=profile.language,
        birth_date=profile.birth_date,
        gender=profile.gender,
        inventory=profile.inventory.model_dump(),
        clan=profile.clan.model_dump() if profile.clan else None,
        custom_field=profile.custom_field
    )