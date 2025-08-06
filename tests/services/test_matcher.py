import pytest

from app.domain.services.matcher import ProfileMatcherService
from app.domain.exceptions import PlayerNotFoundError

class DummyProfileRepo:
    def __init__(self, store):
        self.store = store

    def get_by_id(self, player_id):
        if player_id not in self.store:
            raise PlayerNotFoundError()
        return self.store[player_id]

    def save(self, profile):
        self.store[profile.player_id] = profile


class DummyCampaignFetcher:
    def __init__(self, campaigns):
        self.campaigns = campaigns

    def get_current_campaigns(self):
        return self.campaigns

def test_matches_and_updates_profile(base_profile, base_campaign, now):
    repo = DummyProfileRepo({'test_player': base_profile})
    fetcher = DummyCampaignFetcher([base_campaign])
    service = ProfileMatcherService(fetcher, repo)

    result = service.match_profile('test_player', now)

    assert 'test_campaign' in result.active_campaigns


def test_skips_inactive_campaign(base_profile, base_campaign, now):
    base_campaign.enabled = False
    repo = DummyProfileRepo({'test_player': base_profile})
    fetcher = DummyCampaignFetcher([base_campaign])
    service = ProfileMatcherService(fetcher, repo)

    result = service.match_profile('test_player', now)

    assert result.active_campaigns == []


def test_skips_if_not_matching(base_profile, base_campaign, now):
    base_profile.level = 99  
    repo = DummyProfileRepo({'test_player': base_profile})
    fetcher = DummyCampaignFetcher([base_campaign])
    service = ProfileMatcherService(fetcher, repo)

    result = service.match_profile('test_player', now)

    assert result.active_campaigns == []


def test_raises_player_not_found(base_campaign, now):
    repo = DummyProfileRepo({})
    fetcher = DummyCampaignFetcher([base_campaign])
    service = ProfileMatcherService(fetcher, repo)

    with pytest.raises(PlayerNotFoundError):
        service.match_profile('unknown', now)