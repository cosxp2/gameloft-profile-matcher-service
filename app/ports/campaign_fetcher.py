from abc import ABC, abstractmethod
from typing import List
from app.domain.models.campaign import Campaign

class CampaignFetcher(ABC):
    @abstractmethod
    def get_current_campaigns(self) -> List[Campaign]:
        pass