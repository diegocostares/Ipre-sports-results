from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from src.database.database import Base


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    league_division = Column(String(10), comment="League Division")
    match_date = Column(Date, comment="Match Date (dd/mm/yy)")
    kick_off_time = Column(Time, comment="Time of match kick off")
    home_team_name = Column(String(50), comment="Home Team")
    away_team_name = Column(String(50), comment="Away Team")
    full_time_home_goals = Column(Integer, comment="Full Time Home Team Goals")
    full_time_away_goals = Column(Integer, comment="Full Time Away Team Goals")
    full_time_result = Column(String(1), comment="Full Time Result (H=Home Win, D=Draw, A=Away Win)")
    half_time_home_goals = Column(Integer, comment="Half Time Home Team Goals")
    half_time_away_goals = Column(Integer, comment="Half Time Away Team Goals")
    half_time_result = Column(String(1), comment="Half Time Result (H=Home Win, D=Draw, A=Away Win)")
    referee = Column(String(50), comment="Match Referee")

    # Relación con el modelo de estadísticas
    match_statistics = relationship("MatchStatistics", back_populates="match", uselist=False)

