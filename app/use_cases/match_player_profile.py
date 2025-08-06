from datetime import datetime, timezone
from app.domain.models.player import PlayerProfile
from app.domain.services.matcher import ProfileMatcherService


class MatchPlayerProfileUseCase:
    def __init__(self, matcher_service: ProfileMatcherService):
        self.matcher_service = matcher_service

    def execute(self, player_id: str, now: datetime | None = None) -> PlayerProfile:
        now = now or datetime.now(timezone.utc)
        return self.matcher_service.match_profile(player_id, now)