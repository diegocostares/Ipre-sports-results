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
    home_score = Column(Integer, comment="Home Team Score at Full Time")
    away_score = Column(Integer, comment="Away Team Score at Full Time")
    posession_home = Column(Float, comment="Home Team Possession Percentage")
    posession_away = Column(Float, comment="Away Team Possession Percentage")
    total_shots_home = Column(Integer, comment="Total Shots by Home Team")
    total_shots_away = Column(Integer, comment="Total Shots by Away Team")
    shots_on_target_home = Column(Integer, comment="Shots on Target by Home Team")
    shots_on_target_away = Column(Integer, comment="Shots on Target by Away Team")
    shots_off_target_home = Column(Integer, comment="Shots off Target by Home Team")
    shots_off_target_away = Column(Integer, comment="Shots off Target by Away Team")
    blocked_shots_home = Column(Integer, comment="Blocked Shots by Home Team")
    blocked_shots_away = Column(Integer, comment="Blocked Shots by Away Team")
    corner_kicks_home = Column(Integer, comment="Corner Kicks by Home Team")
    corner_kicks_away = Column(Integer, comment="Corner Kicks by Away Team")
    offsides_home = Column(Integer, comment="Offsides by Home Team")
    offsides_away = Column(Integer, comment="Offsides by Away Team")
    fouls_home = Column(Integer, comment="Fouls Committed by Home Team")
    fouls_away = Column(Integer, comment="Fouls Committed by Away Team")
    yellow_cards_home = Column(Integer, comment="Yellow Cards to Home Team")
    yellow_cards_away = Column(Integer, comment="Yellow Cards to Away Team")
    red_cards_home = Column(Integer, comment="Red Cards to Home Team")
    red_cards_away = Column(Integer, comment="Red Cards to Away Team")
    free_kicks_home = Column(Integer, comment="Free Kicks won by Home Team")
    free_kicks_away = Column(Integer, comment="Free Kicks won by Away Team")
    throw_ins_home = Column(Integer, comment="Throw Ins taken by Home Team")
    throw_ins_away = Column(Integer, comment="Throw Ins taken by Away Team")
    goal_kicks_home = Column(Integer, comment="Goal Kicks taken by Home Team")
    goal_kicks_away = Column(Integer, comment="Goal Kicks taken by Away Team")
    big_chances_home = Column(Integer, comment="Big Chances created by Home Team")
    big_chances_away = Column(Integer, comment="Big Chances created by Away Team")
    big_chances_missed_home = Column(Integer, comment="Big Chances missed by Home Team")
    big_chances_missed_away = Column(Integer, comment="Big Chances missed by Away Team")
    hit_woodwork_home = Column(Integer, comment="Times Home Team hit the Woodwork")
    hit_woodwork_away = Column(Integer, comment="Times Away Team hit the Woodwork")
    counter_attacks_home = Column(Integer, comment="Counter Attacks by Home Team")
    counter_attacks_away = Column(Integer, comment="Counter Attacks by Away Team")
    counter_attacks_shots_home = Column(Integer, comment="Shots from Counter Attacks by Home Team")
    counter_attacks_shots_away = Column(Integer, comment="Shots from Counter Attacks by Away Team")
    shots_inside_box_home = Column(Integer, comment="Shots Inside the Box by Home Team")
    shots_inside_box_away = Column(Integer, comment="Shots Inside the Box by Away Team")
    shots_outside_box_home = Column(Integer, comment="Shots Outside the Box by Home Team")
    shots_outside_box_away = Column(Integer, comment="Shots Outside the Box by Away Team")
    goalkeeper_saves_home = Column(Integer, comment="Goalkeeper Saves by Home Team")
    goalkeeper_saves_away = Column(Integer, comment="Goalkeeper Saves by Away Team")
    passes_home = Column(Integer, comment="Total Passes by Home Team")
    passes_away = Column(Integer, comment="Total Passes by Away Team")
    accurate_passes_home = Column(Integer, comment="Accurate Passes by Home Team")
    accurate_passes_away = Column(Integer, comment="Accurate Passes by Away Team")
    long_balls_home = Column(Integer, comment="Long Balls by Home Team")
    long_balls_away = Column(Integer, comment="Long Balls by Away Team")
    crosses_home = Column(Integer, comment="Crosses by Home Team")
    crosses_away = Column(Integer, comment="Crosses by Away Team")
    dribbles_home = Column(Integer, comment="Dribbles by Home Team")
    dribbles_away = Column(Integer, comment="Dribbles by Away Team")
    posession_lost_home = Column(Integer, comment="Possession Lost by Home Team")
    posession_lost_away = Column(Integer, comment="Possession Lost by Away Team")
    duels_won_home = Column(Integer, comment="Duels Won by Home Team")
    duels_won_away = Column(Integer, comment="Duels Won by Away Team")
    aerials_won_home = Column(Integer, comment="Aerial Duels Won by Home Team")
    aerials_won_away = Column(Integer, comment="Aerial Duels Won by Away Team")
    tackles_home = Column(Integer, comment="Tackles Made by Home Team")
    tackles_away = Column(Integer, comment="Tackles Made by Away Team")
    interceptions_home = Column(Integer, comment="Interceptions by Home Team")
    interceptions_away = Column(Integer, comment="Interceptions by Away Team")
    clearences_home = Column(Integer, comment="Clearances by Home Team")
    clearences_away = Column(Integer, comment="Clearances by Away Team")

    match = relationship("Match", back_populates="match_statistics")