def test_get_item_quantity_existing(base_profile):
    assert base_profile.inventory.get_item_quantity('item_1') == 2

def test_get_item_quantity_missing(base_profile):
    assert base_profile.inventory.get_item_quantity('item_999') == 0

def test_get_all_items(base_profile):
    items = base_profile.inventory.get_all_items()
    assert items == {'item_1': 2, 'item_2': 0, 'item_3': 1}
    assert isinstance(items, dict)

def test_add_active_campaign(base_profile):
    base_profile.add_active_campaign('test_campaign')
    assert 'test_campaign' in base_profile.active_campaigns

def test_add_active_campaign_does_not_duplicate(base_profile):
    base_profile.active_campaigns = ['test_campaign']
    base_profile.add_active_campaign('test_campaign')
    assert base_profile.active_campaigns.count('test_campaign') == 1