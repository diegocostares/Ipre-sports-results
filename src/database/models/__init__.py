from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .bookmaker_odds import BookmakerOdds
from .bookmakers import Bookmaker
from .countries import Country
from .leagues import League
from .statistics import Statistics

__all__ = ["Country", "League", "Statistics", "Bookmaker", "BookmakerOdds"]