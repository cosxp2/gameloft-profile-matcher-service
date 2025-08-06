from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerProfileDBModel(Base):
    __tablename__ = "player_profiles"

    player_id = Column(String, primary_key=True, index=True)
    credential = Column(String, nullable=False)

    created = Column(DateTime, nullable=False)
    modified = Column(DateTime, nullable=False)
    last_session = Column(DateTime, nullable=False)

    total_spent = Column(Float, nullable=False)
    total_refund = Column(Float, nullable=False)
    total_transactions = Column(Integer, nullable=False)
    last_purchase = Column(DateTime, nullable=False)

    active_campaigns = Column(JSON, nullable=False)
    devices = Column(JSON, nullable=False)
    level = Column(Integer, nullable=False)
    xp = Column(Integer, nullable=False)
    total_playtime = Column(Float, nullable=False)
    country = Column(String, nullable=False)
    language = Column(String, nullable=False)
    birth_date = Column(DateTime, nullable=False)
    gender = Column(String, nullable=False)

    inventory = Column(JSON, nullable=False)
    clan = Column(JSON, nullable=True)
    custom_field = Column(String, nullable=True)