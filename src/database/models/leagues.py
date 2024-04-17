from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship

from src.database.database import Base


class League(Base):
    __tablename__ = "leagues"
    league_name = Column(String(255), primary_key=True)
    country_name = Column(String(255), ForeignKey("countries.country_name"))

    country = relationship("Country", back_populates="leagues")
    matches = relationship("Match", back_populates="league")
