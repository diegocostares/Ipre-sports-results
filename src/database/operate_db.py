from datetime import datetime

from sqlalchemy.orm import Session

from src.database.database import add_record, create_session
from src.database.models import Match


def create_match(session: Session, match_data: dict):
    """
    Crea y guarda un nuevo partido en la base de datos utilizando los datos proporcionados.
    """
    if "match_date" in match_data and isinstance(match_data["match_date"], str):
        match_data["match_date"] = datetime.strptime(match_data["match_date"], "%Y-%m-%d").date()
    if "kick_off_time" in match_data and isinstance(match_data["kick_off_time"], str):
        match_data["kick_off_time"] = datetime.strptime(match_data["kick_off_time"], "%H:%M").time()
    new_match = Match(**match_data)
    add_record(session, new_match)
    return new_match


def get_all_matches(session: Session):
    """
    Recupera todos los partidos de la base de datos y los retorna.
    """
    matches = session.query(Match).all()
    return matches




if __name__ == "__main__":
    # Para testear algunas cosas
    # ejecutar: poetry run python -m database.operate_db
    session = create_session()
    match_data = {
        # "league_division": "Premier League",
        "match_date": "2023-04-14",
        "kick_off_time": "15:00",
        "home_team_name": "Team A",
        "away_team_name": "Team B",
        "full_time_home_goals": 2,
        "full_time_away_goals": 1,
        "full_time_result": "H",
    }
    match = create_match(session, match_data)
    print(f"Match created: {match.id}")
    matches = get_all_matches(session)
    print(f"Total matches: {len(matches)}")
    session.close()
