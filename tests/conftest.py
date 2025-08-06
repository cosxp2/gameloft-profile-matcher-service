import pytest
from datetime import datetime, timedelta, timezone
from app.adapters.db.sqlalchemy_models import Base
from app.adapters.dependencies import engine
from app.domain.models.player import PlayerProfile, Inventory, Device, Clan
from app.domain.models.campaign import (
    Campaign, CampaignMatchers, LevelMatcher, HasMatcher, DoesNotHaveMatcher
)

@pytest.fixture
def now():
    return datetime.now(timezone.utc)


@pytest.fixture
def base_matcher():
    return CampaignMatchers(
        level=LevelMatcher(min=1, max=10),
        has=HasMatcher(country=['RO'], items=['item_1']),
        does_not_have=DoesNotHaveMatcher(items=['item_2'])
    )


@pytest.fixture
def base_campaign(base_matcher, now):
    return Campaign(
        game='test_game',
        name='test_campaign',
        priority=10.0,
        matchers=base_matcher,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(days=1),
        enabled=True,
        last_updated=now
    )


@pytest.fixture
def base_inventory():
    return Inventory(
        cash=100.0,
        coins=50,
        items={'item_1': 2, 'item_2': 0, 'item_3': 1}
    )


@pytest.fixture
def base_profile(base_inventory, now):
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
def base_profile_db_entry(base_profile):
    from utils.conversions import domain_to_db_model
    return domain_to_db_model(base_profile)

@pytest.fixture(autouse=True)
def clean_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)