from typing import List
from app.ports.campaign_fetcher import CampaignFetcher
from app.domain.models.campaign import Campaign

class StubCampaignFetcher(CampaignFetcher):
    def __init__(self, campaigns: List[Campaign]):
        self._campaigns = campaigns

    def get_current_campaigns(self) -> List[Campaign]:
        return self._campaigns