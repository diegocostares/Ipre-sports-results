from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship

from src.database.database import Base


class Bookmaker(Base):
    __tablename__ = "bookmakers"
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    match_id = Column(Integer, ForeignKey("matches.id"))

    match = relationship("Match", back_populates="bookmakers")
    odds = relationship("BookmakerOdds", back_populates="bookmaker")
