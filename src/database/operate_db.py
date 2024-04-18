import json
from datetime import datetime

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, class_mapper, sessionmaker

from src.database.database import Base, add_record, create_session
from src.database.models import Bookmaker, BookmakerOdds, Country, League, Statistics


def create_match(session: Session, match_data: dict):
    """
    Crea y guarda un nuevo partido en la base de datos utilizando los datos proporcionados.
    """
    if "date" in match_data and isinstance(match_data["date"], str):
        match_data["date"] = datetime.strptime(match_data["date"], "%Y-%m-%d").date()
    if "kick_off_time" in match_data and isinstance(match_data["kick_off_time"], str):
        match_data["kick_off_time"] = datetime.strptime(match_data["kick_off_time"], "%H:%M").time()
    new_match = Statistics(**match_data)
    add_record(session, new_match)
    return new_match


def get_all_matches(session: Session):
    """
    Recupera todos los partidos de la base de datos y los retorna.
    """
    matches = session.query(Statistics).all()
    return matches


def load_data_from_json(url_json="src/tests/initial_data.json"):
    with open(url_json, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def populate_database(session, data):
    # Poblar países
    for country_data in data.get("countries", []):
        country = Country(**country_data)
        session.add(country)

    # Poblar ligas
    for league_data in data.get("leagues", []):
        league = League(**league_data)
        session.add(league)

    # Poblar estadisticas generales de partidos
    for match_data in data.get("statistics", []):
        match_data["date"] = datetime.strptime(match_data["date"], "%Y-%m-%d").date()
        match_data["kick_off_time"] = datetime.strptime(match_data["kick_off_time"], "%H:%M").time()
        match = Statistics(**match_data)
        session.add(match)

    # Poblar casas de apuestas
    for bookmaker_data in data.get("bookmakers", []):
        bookmaker = Bookmaker(**bookmaker_data)
        session.add(bookmaker)

    # Poblar odds
    for odds_data in data.get("bookmaker_odds", []):
        odds = BookmakerOdds(**odds_data)
        session.add(odds)

    session.commit()



def get_columns(model):
    """Helper function to get column attributes of a SQLAlchemy model in a format for querying."""
    return [
        getattr(model, column.name).label(f"{model.__tablename__}_{column.name}")
        for column in class_mapper(model).columns
    ]


def fetch_data_as_dataframe():
    session = create_session()
    try:
        country_columns = get_columns(Country)
        league_columns = get_columns(League)
        statistics = get_columns(Statistics)
        odds_columns = get_columns(BookmakerOdds)

        basic_query = (
            session.query(*country_columns, *league_columns, *statistics)
            .join(League, Country.country_name == League.country_name)
            .join(Statistics, League.league_name == Statistics.league_name)
        )
        df_basic = pd.read_sql(basic_query.statement, session.bind)

        bookmaker_columns = [Bookmaker.name.label("bookmaker_name")]
        odds_query = (
            session.query(Statistics.id.label("statistics_id"), *bookmaker_columns, *odds_columns)
            .join(Bookmaker, Statistics.id == Bookmaker.statistics_id)
            .join(BookmakerOdds, Bookmaker.id == BookmakerOdds.bookmaker_id)
        )
        df_odds = pd.read_sql(odds_query.statement, session.bind)

        if not df_odds.empty:
            df_odds_pivot = df_odds.pivot_table(index="statistics_id", columns="bookmaker_name", aggfunc="first")
            df_odds_pivot.columns = [f"{a}_{b.lower().replace(' ', '_')}" for a, b in df_odds_pivot.columns]
            df_basic = df_basic.merge(df_odds_pivot, left_on="statistics_id", right_index=True, how="left")

    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()

    finally:
        session.close()

    return df_basic


def transform_and_save_csv(df):
    df.to_csv("output.csv", index=False)


if __name__ == "__main__":
    # Para testear algunas cosas
    # ejecutar: poetry run python -m database.operate_db
    session = create_session()
    data = load_data_from_json()
    populate_database(session, data)


    session.close()

    df = fetch_data_as_dataframe()
    transform_and_save_csv(df)
