import pytest
from datetime import datetime, timedelta, timezone
from app.domain.models.campaign import(
    LevelMatcher,
    HasMatcher, 
    DoesNotHaveMatcher, 
    CampaignMatchers,
    Campaign
)

@pytest.fixture
def base_matchers():
    return CampaignMatchers(
        level=LevelMatcher(min=1, max=10),
        has=HasMatcher(country=['RO'], items=['item_1']),
        does_not_have=DoesNotHaveMatcher(items=['item_2'])
    )

@pytest.fixture
def base_campaign(base_matchers):
    now = datetime.now(timezone.utc)
    
    return Campaign(
        game='mygame',
        name='mycampaign',
        priority=10.0,
        matchers=base_matchers,
        start_date=now - timedelta(days=1),
        end_date=now + timedelta(days=1),
        enabled=True,
        last_updated=now
    )

@pytest.fixture
def now():
    return datetime.now(timezone.utc)

def test_campaign_is_active_now(base_campaign, now):    
    assert base_campaign.is_active(now)
    
def test_campaign_is_disabled(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        "enabled": False
    })

    assert not campaign.is_active(now)
    
def test_campaign_before_start_date(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        "start_date": now + timedelta(days=1)
    })
    
    assert not campaign.is_active(now)

def test_campaign_after_end_date(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        "end_date": now - timedelta(days=1)
    })
    
    assert not campaign.is_active(now)

def test_campaign_start_and_end_now(base_campaign, now):
    campaign = base_campaign.model_copy(update={
        "start_date": now,
        "end_date": now
    })
    
    assert campaign.is_active(now)
    