import json
import pytest
from datetime import datetime, timezone
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel, Base
from app.adapters.dependencies import engine, SessionLocal
from app.main import app
from utils.conversions import domain_to_db_model

client = TestClient(app)

@pytest.fixture
def seed_test_player(base_profile_db_entry):
    db: Session = SessionLocal()
    db.add(base_profile_db_entry)
    db.commit()
    db.close()

@pytest.mark.usefixtures('seed_test_player')
def test_get_client_config_success():
    response = client.get('/get_client_config/test_player')
    assert response.status_code == 200
    data = response.json()
    assert data['player_id'] == 'test_player'
    assert data['active_campaigns'] == ['mycampaign']
