from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship
from . import Base

# Declaración de Base para los modelos

class Country(Base):
    __tablename__ = "countries"
    country_name = Column(String(255), primary_key=True)
    country_acronym = Column(String(10), nullable=False)

    leagues = relationship("League", back_populates="country")
