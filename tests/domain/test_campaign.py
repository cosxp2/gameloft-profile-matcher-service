from datetime import timedelta

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