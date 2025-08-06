from datetime import datetime
from typing import List, Dict
from pydantic import BaseModel, Field, Optional
from campaign import Campaign

class Device(BaseModel):
    id: int
    model: str
    carrier: str
    firmware: str
    
class Inventory(BaseModel):    
    cash: float = 0.0
    coins: int = 0
    items: Dict[str, int] = Field(default_factory=dict)

    def get_item_quantity(self, item_name: str) -> int:
        return self.items.get(item_name, 0)

    def get_all_items(self) -> Dict[str, int]:
        return self.items
    
class Clan(BaseModel):
    id: int
    name: str

class PlayerProfile(BaseModel):
    player_id: str
    credential: str
    created: datetime
    modified: datetime
    last_session: datetime
    total_spent: float
    total_refund: float
    total_transactions: int
    last_purchase: datetime
    active_campaigns: List[str] = Field(default_factory=list)
    devices: List[Device]
    level: int
    xp: int
    total_playtime: float
    country: str
    language: str
    birth_date: datetime
    gender: str
    inventory: Inventory
    clan: Optional[Clan] = None
    custom_field: Optional[str] = None
    
    def add_active_campaign(self, campaign_name: str) -> None:
        if campaign_name not in self.active_campaigns:
            self.active_campaigns.append(campaign_name)