from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import relationship

from src.database.database import Base


class MatchStatistics(Base):
    __tablename__ = "match_statistics"
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey("matches.id"))
    crowd_attendance = Column(Integer, comment="Crowd Attendance")
    home_team_shots = Column(Integer, comment="Home Team Shots")
    away_team_shots = Column(Integer, comment="Away Team Shots")
    home_team_shots_on_target = Column(Integer, comment="Home Team Shots on Target")
    away_team_shots_on_target = Column(Integer, comment="Away Team Shots on Target")
    home_team_hit_woodwork = Column(Integer, comment="Home Team Hit Woodwork")
    away_team_hit_woodwork = Column(Integer, comment="Away Team Hit Woodwork")
    home_team_corners = Column(Integer, comment="Home Team Corners")
    away_team_corners = Column(Integer, comment="Away Team Corners")
    home_team_fouls_committed = Column(Integer, comment="Home Team Fouls Committed")
    away_team_fouls_committed = Column(Integer, comment="Away Team Fouls Committed")
    home_team_offsides = Column(Integer, comment="Home Team Offsides")
    away_team_offsides = Column(Integer, comment="Away Team Offsides")
    home_team_yellow_cards = Column(Integer, comment="Home Team Yellow Cards")
    away_team_yellow_cards = Column(Integer, comment="Away Team Yellow Cards")
    home_team_red_cards = Column(Integer, comment="Home Team Red Cards")
    away_team_red_cards = Column(Integer, comment="Away Team Red Cards")
    home_team_bookings_points = Column(Integer, comment="Home Team Bookings Points (10 = yellow, 25 = red)")
    away_team_bookings_points = Column(Integer, comment="Away Team Bookings Points (10 = yellow, 25 = red)")

    match = relationship("Match", back_populates="match_statistics")

