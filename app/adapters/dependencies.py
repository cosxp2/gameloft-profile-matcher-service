from datetime import datetime, timezone, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.adapters.db.sqlalchemy_models import Base
from app.adapters.db.sqlalchemy_player_repo import SqlAlchemyPlayerRepo
from app.adapters.campaign_api.stub_campaign_fetcher import StubCampaignFetcher
from app.domain.services.matcher import ProfileMatcherService
from app.domain.models.campaign import CampaignMatchers, Campaign
from app.domain.models.campaign import LevelMatcher, HasMatcher, DoesNotHaveMatcher
from app.use_cases.match_player_profile import MatchPlayerProfileUseCase

engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def get_match_player_use_case() -> MatchPlayerProfileUseCase:
    repo = SqlAlchemyPlayerRepo(SessionLocal)

    # Set up mocked campaigns
    campaigns = [
        Campaign(
            game="mygame",
            name="mycampaign",
            priority=10.5,
            matchers=CampaignMatchers(
                level=LevelMatcher(min=1, max=10),
                has=HasMatcher(country=["RO"], items=["item_1"]),
                does_not_have=DoesNotHaveMatcher(items=["item_4"])
            ),
            start_date=datetime.now(timezone.utc) - timedelta(days=1),
            end_date=datetime.now(timezone.utc) + timedelta(days=5),
            enabled=True,
            last_updated=datetime.now(timezone.utc)
        )
    ]

    # Inject stub and repo into the service
    fetcher = StubCampaignFetcher(campaigns)
    service = ProfileMatcherService(campaign_fetcher=fetcher, profile_repository=repo)

    # Return the use case with all dependencies 
    return MatchPlayerProfileUseCase(service)