import pytest
from datetime import datetime, timezone
from app.domain.models.player import PlayerProfile, Inventory, Device, Clan
from app.domain.models.campaign import Campaign  

@pytest.fixture
def base_inventory():
    return Inventory(
        cash=100.0,
        coins=50,
        items={'item_1': 2, 'item_2': 5}
    )

@pytest.fixture
def base_player(base_inventory, now):
    return PlayerProfile(
        player_id='test_player',
        credential='apple',
        created=now,
        modified=now,
        last_session=now,
        total_spent=100.0,
        total_refund=0.0,
        total_transactions=3,
        last_purchase=now,
        active_campaigns=[],
        devices=[Device(id=1, model='iPhone 11', carrier='vodafone', firmware='16.4')],
        level=5,
        xp=1200,
        total_playtime=80.0,
        country='RO',
        language='ro',
        birth_date=datetime(2000, 1, 1, tzinfo=timezone.utc),
        gender='male',
        inventory=base_inventory,
        clan=Clan(id=42, name='test_clan'),
        custom_field='test_field'
    )
    
@pytest.fixture
def now():
    return datetime.now(timezone.utc)

def test_get_item_quantity_existing(base_player):
    assert base_player.inventory.get_item_quantity('item_1') == 2

def test_get_item_quantity_missing(base_player):
    assert base_player.inventory.get_item_quantity('item_999') == 0

def test_get_all_items(base_player):
    items = base_player.inventory.get_all_items()
    assert items == {'item_1': 2, 'item_2': 5}
    assert isinstance(items, dict)

def test_add_active_campaign(base_player):
    base_player.add_active_campaign('test_campaign')
    assert 'test_campaign' in base_player.active_campaigns

def test_add_active_campaign_does_not_duplicate(base_player):
    base_player.active_campaigns = ['test_campaign']
    base_player.add_active_campaign('test_campaign')
    assert base_player.active_campaigns.count('test_campaign') == 1