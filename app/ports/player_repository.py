from abc import ABC, abstractmethod
from app.domain.models.player import PlayerProfile

class PlayerProfileRepository(ABC):
    @abstractmethod
    def get_by_id(self, player_id: str) -> PlayerProfile:
        pass
    
    @abstractmethod
    def save(self, profile: PlayerProfile) -> None:
        pass