from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

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