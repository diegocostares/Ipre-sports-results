from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship

from src.database.database import Base


class Country(Base):
    __tablename__ = "countries"
    country_name = Column(String(255), primary_key=True)
    country_acronym = Column(String(10), nullable=False)

    leagues = relationship("League", back_populates="country")
