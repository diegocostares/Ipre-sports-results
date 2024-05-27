import pandas as pd
import os.path as pt
from models.statistics import Statistics

def read_csv_and_transform_statistics(csv_file):
    if not pt.exists(csv_file):
        raise FileNotFoundError(f"El archivo {csv_file} no existe.")
    df = pd.read_csv(csv_file)
    
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d").dt.strftime("%d/%m/%y")
    
    if "kick_off_time" in df.columns:
        df["kick_off_time"] = pd.to_datetime(df["kick_off_time"], format="%H:%M").dt.time
    
    if "full_time_result" in df.columns:
        df[["full_time_home_goals", "full_time_away_goals"]] = df["full_time_result"].str.split("-", expand=True)
        df[["full_time_home_goals", "full_time_away_goals"]] = df[["full_time_home_goals", "full_time_away_goals"]].astype(int)
    
    if "half_time_result" in df.columns:
        df[["half_time_home_goals", "half_time_away_goals"]] = df["half_time_result"].str.split("-", expand=True)
        df[["half_time_home_goals", "half_time_away_goals"]] = df[["half_time_home_goals", "half_time_away_goals"]].astype(int)
    
    df["home_team_name"] = df["home_team_name"].str.lower()
    df["away_team_name"] = df["away_team_name"].str.lower()
    df["league_name"] = df["league_name"].str.lower()
    
    df["home_team_name"] = df["home_team_name"].astype(str)
    df["away_team_name"] = df["away_team_name"].astype(str)
    df["league_name"] = df["league_name"].astype(str)
    
    null_columns = df.columns[df.isnull().any()]
    if len(null_columns) > 0:
        print(f"Las columnas con valores nulos son: {null_columns}")
        for column in null_columns:
            if df[column].dtype == "object":
                df[column] = df[column].fillna("Unknown")
            else:
                df[column] = df[column].fillna(0)
    
    return df

def populate_database_from_csv_statistics(csv_file):
    df = read_csv_and_transform_statistics(csv_file)
    matches = []
    
    for index, row in df.iterrows():
        try:
            new_match = Statistics(
                league_name=row.get("league_name", "Unknown"),
                date=row.get("date", None),
                kick_off_time=row.get("kick_off_time", None),
                home_team_name=row.get("home_team_name", "Unknown"),
                away_team_name=row.get("away_team_name", "Unknown"),
                full_time_home_goals=row.get("full_time_home_goals", 0),
                full_time_away_goals=row.get("full_time_away_goals", 0),
                full_time_result=row.get("full_time_result", "Unknown"),
                half_time_home_goals=row.get("half_time_home_goals", 0),
                half_time_away_goals=row.get("half_time_away_goals", 0),
                half_time_result=row.get("half_time_result", "Unknown"),
                referee=row.get("referee", "Unknown"),
                crowd_attendance=row.get("crowd_attendance", 0),
                home_team_shots=row.get("home_team_shots", 0),
                away_team_shots=row.get("away_team_shots", 0),
                home_team_shots_on_target=row.get("home_team_shots_on_target", 0),
                away_team_shots_on_target=row.get("away_team_shots_on_target", 0),
                home_team_hit_woodwork=row.get("home_team_hit_woodwork", 0),
                away_team_hit_woodwork=row.get("away_team_hit_woodwork", 0),
                home_team_corners=row.get("home_team_corners", 0),
                away_team_corners=row.get("away_team_corners", 0),
                home_team_fouls_committed=row.get("home_team_fouls_committed", 0),
                away_team_fouls_committed=row.get("away_team_fouls_committed", 0),
                home_team_offsides=row.get("home_team_offsides", 0),
                away_team_offsides=row.get("away_team_offsides", 0),
                home_team_yellow_cards=row.get("home_team_yellow_cards", 0),
                away_team_yellow_cards=row.get("away_team_yellow_cards", 0),
                home_team_red_cards=row.get("home_team_red_cards", 0),
                away_team_red_cards=row.get("away_team_red_cards" , 0),
                home_team_bookings_points=row.get("home_team_bookings_points", 0),
                away_team_bookings_points=row.get("away_team_bookings_points", 0),
                home_score=row.get("home_score", 0),
                away_score=row.get("away_score", 0),
                posession_home=row.get("posession_home", 0),
                posession_away=row.get("posession_away", 0),
                total_shots_home=row.get("total_shots_home", 0),
                total_shots_away=row.get("total_shots_away", 0),
                shots_on_target_home=row.get("shots_on_target_home", 0),
                shots_on_target_away=row.get("shots_on_target_away", 0),
                shots_off_target_home=row.get("shots_off_target_home", 0),
                shots_off_target_away=row.get("shots_off_target_away", 0),
                blocked_shots_home=row.get("blocked_shots_home", 0),
                blocked_shots_away=row.get("blocked_shots_away", 0),
                corner_kicks_home=row.get("corner_kicks_home", 0),
                corner_kicks_away=row.get("corner_kicks_away", 0),
                offsides_home=row.get("offsides_home", 0), 
                offsides_away=row.get("offsides_away", 0),
                fouls_home=row.get("fouls_home", 0),
                fouls_away=row.get("fouls_away", 0),
                yellow_cards_home=row.get("yellow_cards_home", 0),
                yellow_cards_away=row.get("yellow_cards_away", 0),
                red_cards_home=row.get("red_cards_home", 0),
                red_cards_away=row.get("red_cards_away", 0),
                free_kicks_home=row.get("free_kicks_home", 0),
                free_kicks_away=row.get("free_kicks_away", 0),
                throw_ins_home=row.get("throw_ins_home", 0),
                throw_ins_away=row.get("throw_ins_away", 0),
                goal_kicks_home=row.get("goal_kicks_home", 0),
                goal_kicks_away=row.get("goal_kicks_away", 0),
                big_chances_home=row.get("big_chances_home", 0),
                big_chances_away=row.get("big_chances_away", 0),
                big_chances_missed_home=row.get("big_chances_missed_home", 0),
                big_chances_missed_away=row.get("big_chances_missed_away", 0),
                hit_woodwork_home=row.get("hit_woodwork_home", 0),
                hit_woodwork_away=row.get("hit_woodwork_away", 0),
                counter_attacks_home=row.get("counter_attacks_home", 0),
                counter_attacks_away=row.get("counter_attacks_away", 0),
                counter_attacks_shots_home=row.get("counter_attacks_shots_home", 0),
                counter_attacks_shots_away=row.get("counter_attacks_shots_away", 0),
                shots_inside_box_home=row.get("shots_inside_box_home", 0),
                shots_inside_box_away=row.get("shots_inside_box_away", 0),
                shots_outside_box_home=row.get("shots_outside_box_home", 0),
                shots_outside_box_away=row.get("shots_outside_box_away", 0),
                goalkeeper_saves_home=row.get("goalkeeper_saves_home", 0),
                goalkeeper_saves_away=row.get("goalkeeper_saves_away", 0),
                passes_total_home=row.get("passes_total_home", 0),
                passes_total_away=row.get("passes_total_away", 0),
                passes_accurate_home=row.get("passes_accurate_home", 0),
                passes_accurate_away=row.get("passes_accurate_away", 0),
                passes_accuracy_home=row.get("passes_accuracy_home", 0.0),
                passes_accuracy_away=row.get("passes_accuracy_away", 0.0),
                key_passes_home=row.get("key_passes_home", 0),
                key_passes_away=row.get("key_passes_away", 0),
                crosses_home=row.get("crosses_home", 0),
                crosses_away=row.get("crosses_away", 0),
                crosses_accuracy_home=row.get("crosses_accuracy_home", 0.0),
                crosses_accuracy_away=row.get("crosses_accuracy_away", 0.0),
                long_balls_home=row.get("long_balls_home", 0),
                long_balls_away=row.get("long_balls_away", 0),
                long_balls_accuracy_home=row.get("long_balls_accuracy_home", 0.0),
                long_balls_accuracy_away=row.get("long_balls_accuracy_away", 0.0),
                dribbles_attempted_home=row.get("dribbles_attempted_home", 0),
                dribbles_attempted_away=row.get("dribbles_attempted_away", 0),
                dribbles_success_home=row.get("dribbles_success_home", 0),
                dribbles_success_away=row.get("dribbles_success_away", 0),
                dribbles_accuracy_home=row.get("dribbles_accuracy_home", 0.0),
                dribbles_accuracy_away=row.get("dribbles_accuracy_away", 0.0),
                possession_lost_home=row.get("possession_lost_home", 0),
                possession_lost_away=row.get("possession_lost_away", 0),
                duels_won_home=row.get("duels_won_home", 0),
                duels_won_away=row.get("duels_won_away", 0),
                aerial_duels_won_home=row.get("aerial_duels_won_home", 0),
                aerial_duels_won_away=row.get("aerial_duels_won_away", 0),
                tackles_home=row.get("tackles_home", 0),
                tackles_away=row.get("tackles_away", 0),
                interceptions_home=row.get("interceptions_home", 0),
                interceptions_away=row.get("interceptions_away", 0),
                clearances_home=row.get("clearances_home", 0),
                clearances_away=row.get("clearances_away", 0),
                error_lead_to_goal_home=row.get("error_lead_to_goal_home", 0),
                error_lead_to_goal_away=row.get("error_lead_to_goal_away", 0),
                error_lead_to_shot_home=row.get("error_lead_to_shot_home", 0),
                error_lead_to_shot_away=row.get("error_lead_to_shot_away", 0),
            )
            matches.append(new_match)
        except Exception as e:
            print(f"Error al procesar la fila {index}: {e}")
    
    return matches
