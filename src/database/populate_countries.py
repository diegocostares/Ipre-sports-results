import pandas as pd
import os.path as pt
from sqlalchemy.orm import Session
from models.countries import Country

import pandas as pd
import os.path as pt

def read_csv_and_transform_countries(csv_file):
    """
    Lee un archivo CSV y lo transforma en un DataFrame de Pandas.
    """
    if not pt.exists(csv_file):
        raise FileNotFoundError(f"El archivo {csv_file} no existe.")
    
    df = pd.read_csv(csv_file)

    # Asegurarnos que las columnas tengan los nombres correctos
    if "home_team_name" not in df.columns or "away_team_name" not in df.columns:
        raise ValueError("El archivo CSV no tiene las columnas esperadas.")
    
    df["home_team_name"] = df["home_team_name"].str.strip().fillna("Unknown")
    df["away_team_name"] = df["away_team_name"].str.strip().fillna("Unknown")

    df["away_team_name"] = df["away_team_name"].astype(str).str.lower()
    df["home_team_name"] = df["home_team_name"].astype(str).str.lower()


    return df[["home_team_name", "away_team_name"]]

def populate_database_from_csv_countries(session: Session, csv_file):
    """
    Pobla la base de datos a partir de un archivo CSV.
    """
    df = read_csv_and_transform_countries(csv_file)

    # Obtener los países únicos
    unique_countries = pd.concat([df["home_team_name"], df["away_team_name"]]).unique()

    for team_name in unique_countries:
        # Verificar si el país ya existe en la base de datos
        existing_country = session.query(Country).filter(Country.country_name == team_name).first()

        # Si no existe, crear nuevo objeto Country
        if not existing_country:
            try:
                new_country = Country(country_name=team_name,
                                    country_acronym="Unknown")
                session.add(new_country)
                session.commit()
            except Exception as e:
                print(f"Error al insertar el país {team_name}: {e}")
                session.rollback()
        else:
            print(f"El país {team_name} ya existe en la base de datos.")

