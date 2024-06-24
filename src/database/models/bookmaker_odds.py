from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Time
from sqlalchemy.orm import declarative_base, relationship
from . import Base




class BookmakerOdds(Base):
    __tablename__ = "bookmaker_odds"
    id = Column(Integer, primary_key=True, autoincrement=True, comment="Primary key, autoincrement")
    bookmaker_id = Column(String(255), ForeignKey("bookmakers.id"), comment="Foreign key to bookmakers table")
    match_odds_team1_ft = Column(Float, comment="Full-time odds for team 1 winning")
    match_odds_the_draw_ft = Column(Float, comment="Full-time odds for a draw")
    match_odds_team2_ft = Column(Float, comment="Full-time odds for team 2 winning")
    over_under_0_5_under = Column(Float, comment="Odds for under 0.5 goals")
    over_under_0_5_over = Column(Float, comment="Odds for over 0.5 goals")
    over_under_1_5_under = Column(Float, comment="Odds for under 1.5 goals")
    over_under_1_5_over = Column(Float, comment="Odds for over 1.5 goals")
    double_chance_home_or_draw = Column(Float, comment="Odds for home team win or draw")
    double_chance_draw_or_away = Column(Float, comment="Odds for draw or away team win")
    double_chance_home_or_away = Column(Float, comment="Odds for home team win or away team win")
    over_under_2_5_under = Column(Float, comment="Odds for under 2.5 goals")
    over_under_2_5_over = Column(Float, comment="Odds for over 2.5 goals")
    over_under_3_5_under = Column(Float, comment="Odds for under 3.5 goals")
    over_under_3_5_over = Column(Float, comment="Odds for over 3.5 goals")
    over_under_4_5_under = Column(Float, comment="Odds for under 4.5 goals")
    over_under_4_5_over = Column(Float, comment="Odds for over 4.5 goals")
    over_under_5_5_under = Column(Float, comment="Odds for under 5.5 goals")
    over_under_5_5_over = Column(Float, comment="Odds for over 5.5 goals")
    both_teams_to_score_yes = Column(Float, comment="Odds for both teams to score - Yes")
    both_teams_to_score_no = Column(Float, comment="Odds for both teams to score - No")
    half_time_full_time_team1_team1 = Column(Float, comment="Odds for team 1 to lead at halftime and win at full-time")
    half_time_full_time_team1_draw = Column(Float, comment="Odds for team 1 to lead at halftime and draw at full-time")
    half_time_full_time_team1_team2 = Column(
        Float, comment="Odds for team 1 to lead at halftime and team 2 to win at full-time"
    )
    half_time_full_time_draw_team1 = Column(Float, comment="Odds for a draw at halftime and team 1 to win at full-time")
    half_time_full_time_draw_draw = Column(Float, comment="Odds for a draw at halftime and draw at full-time")
    half_time_full_time_draw_team2 = Column(Float, comment="Odds for a draw at halftime and team 2 to win at full-time")
    half_time_full_time_team2_team1 = Column(
        Float, comment="Odds for team 2 to lead at halftime and team 1 to win at full-time"
    )
    half_time_full_time_team2_draw = Column(Float, comment="Odds for team 2 to lead at halftime and draw at full-time")
    half_time_full_time_team2_team2 = Column(Float, comment="Odds for team 2 to lead at halftime and win at full-time")

    bookmaker = relationship("Bookmaker", back_populates="odds")
