from sqlalchemy import Column, String, Float, Integer, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class PlayerProfileDBModel(Base):
    __tablename__ = "player_profiles"

    player_id = Column(String, primary_key=True)
    credential = Column(String)
    created = Column(DateTime)
    modified = Column(DateTime)
    last_session = Column(DateTime)
    total_spent = Column(Float)
    total_refund = Column(Float)
    total_transactions = Column(Integer)
    last_purchase = Column(DateTime)
    active_campaigns = Column(JSON)
    devices = Column(JSON)
    level = Column(Integer)
    xp = Column(Integer)
    total_playtime = Column(Float)
    country = Column(String)
    language = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String)
    inventory = Column(JSON)
    clan = Column(JSON, nullable=True)
    custom_field = Column(String, nullable=True)