from app.domain.models.player import PlayerProfile
from app.domain.models.campaign import Campaign
from typing import List
from datetime import datetime
from app.ports.campaign_fetcher import CampaignFetcher
from app.ports.player_repository import PlayerProfileRepository

class ProfileMatcherService:
    def __init__(self, campaign_fetcher: CampaignFetcher, profile_repository: PlayerProfileRepository):
        self.campaign_fetcher = campaign_fetcher
        self.profile_repository = profile_repository

    def match_profile(self, player_id: str, now: datetime) -> PlayerProfile:
        profile = self.profile_repository.get_by_id(player_id)
        campaigns = self.campaign_fetcher.get_current_campaigns()

        for campaign in campaigns:
            if not campaign.is_active(now):
                continue

            if campaign.matchers.matches(profile):
                profile.add_active_campaign(campaign.name)

        self.profile_repository.save(profile)

        return profile