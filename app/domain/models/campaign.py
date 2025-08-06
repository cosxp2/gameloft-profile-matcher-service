from datetime import datetime
from typing import List
from pydantic import BaseModel, Field
from app.domain.models.player import PlayerProfile

class LevelMatcher(BaseModel):
    min: int
    max: int

class HasMatcher(BaseModel):
    country: List[str] = Field(default_factory=list)
    items: List[str] = Field(default_factory=list)
    
class DoesNotHaveMatcher(BaseModel):
    items: List[str] = Field(default_factory=list)
    
class CampaignMatchers(BaseModel):
    level: LevelMatcher
    has: HasMatcher = Field(default_factory=HasMatcher)
    does_not_have: DoesNotHaveMatcher = Field(default_factory=DoesNotHaveMatcher)
    
    def matches(self, profile: PlayerProfile) -> bool:
        if not (self.level.min <= profile.level <= self.level.max):
            return False

        if self.has.country and profile.country not in self.has.country:
            return False

        if self.has.items:
            for item in self.has.items:
                if profile.inventory.get_item_quantity(item) <= 0:
                    return False

        if self.does_not_have.items:
            for item in self.does_not_have.items:
                if profile.inventory.get_item_quantity(item) > 0:
                    return False

        return True

class Campaign(BaseModel):
    game: str
    name: str
    priority: float
    matchers: CampaignMatchers
    start_date: datetime
    end_date: datetime
    enabled: bool
    last_updated: datetime
    
    def is_active(self, now: datetime) -> bool:
        return self.enabled and self.start_date <= now <= self.end_date