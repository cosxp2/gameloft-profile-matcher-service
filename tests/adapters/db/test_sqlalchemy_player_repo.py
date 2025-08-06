import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from app.adapters.db.sqlalchemy_models import Base, PlayerProfileDBModel
from app.adapters.db.sqlalchemy_player_repo import SqlAlchemyPlayerRepo
from app.domain.models.player import PlayerProfile
from utils.conversions import domain_to_db_model

@pytest.fixture
def db_session_factory():
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)

def test_get_by_id_returns_domain_model(db_session_factory, base_profile_db_entry):
    repo = SqlAlchemyPlayerRepo(db_session_factory)
    
    with db_session_factory() as session:
        session.add(base_profile_db_entry)
        session.commit()

    profile = repo.get_by_id('test_player')

    assert isinstance(profile, PlayerProfile)
    assert profile.player_id == 'test_player'
    assert profile.inventory.cash == 100.0

def test_save_updates_existing_profile(db_session_factory, base_profile_db_entry, now):
    repo = SqlAlchemyPlayerRepo(db_session_factory)

    with db_session_factory() as session:
        session.add(base_profile_db_entry)
        session.commit()

    profile = repo.get_by_id('test_player')
    profile.inventory.cash = 999.0
    profile.modified = now

    repo.save(profile)

    with db_session_factory() as session:
        updated = session.query(PlayerProfileDBModel).filter_by(player_id='test_player').first()
        assert updated.inventory['cash'] == 999.0

def test_duplicate_player_id_not_allowed(base_profile_db_entry, db_session_factory, base_profile):
    # First insert should succeed
    with db_session_factory() as session:
        session.add(base_profile_db_entry)
        session.commit()

    # Create a new instance with the same player_id
    duplicate = domain_to_db_model(base_profile)

    # Second insert with same player_id should fail
    with pytest.raises(IntegrityError):
        with db_session_factory() as session:
            session.add(duplicate)
            session.commit()