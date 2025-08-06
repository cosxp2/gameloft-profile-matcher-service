import json
from datetime import datetime, timezone
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel, Base
from app.adapters.dependencies import engine, SessionLocal
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

def seed():
    db: Session = SessionLocal()

    from datetime import datetime, timezone
import json
from app.adapters.db.sqlalchemy_models import PlayerProfileDBModel
from sqlalchemy.orm import Session

def seed_test_player(db: Session):
    dummy_date = datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc)
    
    test_player = PlayerProfileDBModel(
        player_id="test_player",
        credential="apple",
        created=dummy_date,
        modified=dummy_date,
        last_session=dummy_date,
        total_spent=100.0,
        total_refund=0.0,
        total_transactions=3,
        last_purchase=dummy_date,
        active_campaigns=json.dumps([]),
        devices=json.dumps([
            {
                "id": 1,
                "model": "iPhone",
                "carrier": "vodafone",
                "firmware": "1.0"
            }
        ]),
        level=5,
        xp=1000,
        total_playtime=80.0,
        country="RO",
        language="en",
        birth_date=dummy_date,
        gender="male",
        inventory=json.dumps({
            "cash": 100.0,
            "coins": 50,
            "items": {
                "item_1": 1
            }
        }),
        clan=json.dumps({
            "id": 1,
            "name": "test clan"
        }),
        custom_field="demo"
    )

    db.add(test_player)
    db.commit()

    db.add(test_player)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()