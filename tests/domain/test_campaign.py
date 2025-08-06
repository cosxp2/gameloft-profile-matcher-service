import pytest
from datetime import datetime, timedelta, timezone
from app.domain.models.player import Inventory, Device, PlayerProfile
from app.domain.models.campaign import(
    LevelMatcher,
    HasMatcher, 
    DoesNotHaveMatcher, 
    CampaignMatchers,
    Campaign
)

@pytest.fixture
def base_matcher():
    return CampaignMatchers(
        level=LevelMatcher(min=1, max=10),
        has=HasMatcher(country=['RO'], items=['item_1']),
        does_not_have=DoesNotHaveMatcher(items=['item_2'])
    )

@pytest.fixture
def base_campaign(base_matcher):
    now = datetime.now(timezone.utc)
    
    return Campaign(
        game='mygame',
        name='mycampaign',
        priority=10.0,
        matchers=base_matcher,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(days=1),
        enabled=True,
        last_updated=now
    )

@pytest.fixture
def base_profile():
    return PlayerProfile(
        player_id='123',
        credential='apple',
        created=datetime.now(),
        modified=datetime.now(),
        last_session=datetime.now(),
        total_spent=100.0,
        total_refund=0.0,
        total_transactions=5,
        last_purchase=datetime.now(),
        active_campaigns=[],
        devices=[Device(id=1, model='iPhone', carrier='Vodafone', firmware='1.0')],
        level=5,
        xp=1000,
        total_playtime=50.0,
        country='RO',
        language='en',
        birth_date=datetime(2000, 1, 1),
        gender='male',
        inventory=Inventory(cash=100.0, coins=50, items={'item_1': 1, 'item_2': 0}),
        clan=None,
        custom_field=None
    )

@pytest.fixture
def now():
    return datetime.now(timezone.utc)

def test_campaign_is_active_now(base_campaign, now):    
    assert base_campaign.is_active(now)
    
def test_campaign_is_disabled(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        'enabled': False
    })

    assert not campaign.is_active(now)
    
def test_campaign_before_start_date(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        'start_date': now + timedelta(days=1)
    })
    
    assert not campaign.is_active(now)

def test_campaign_after_end_date(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        'end_date': now - timedelta(days=1)
    })
    
    assert not campaign.is_active(now)

def test_campaign_start_and_end_now(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        'start_date': now,
        'end_date': now
    })
    
    assert campaign.is_active(now)

def test_matcher_success(base_profile, base_matcher):
    assert base_matcher.matches(base_profile) is True

def test_matcher_fails_on_level_too_low(base_profile, base_matcher):
    base_profile.level = 0
    assert base_matcher.matches(base_profile) is False

def test_matcher_fails_on_level_too_high(base_profile, base_matcher):
    base_profile.level = 100
    assert base_matcher.matches(base_profile) is False

def test_matcher_fails_if_country_not_included(base_profile, base_matcher):
    base_profile.country = 'US'
    assert base_matcher.matches(base_profile) is False

def test_matcher_fails_if_required_item_missing(base_profile, base_matcher):
    base_profile.inventory.items['item_1'] = 0
    assert base_matcher.matches(base_profile) is False

def test_matcher_fails_if_forbidden_item_present(base_profile, base_matcher):
    base_profile.inventory.items['item_2'] = 1
    assert base_matcher.matches(base_profile) is False