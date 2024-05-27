import pandas as pd
import os.path as pt
from models.leagues import League

def read_csv_and_transform_leagues(csv_file):
    """
    Lee un archivo CSV y transforma los datos en un DataFrame de Pandas.
    """
    if not pt.exists(csv_file):
        raise FileNotFoundError(f"El archivo {csv_file} no existe.")
    
    df = pd.read_csv(csv_file)
    
    # Asegurarnos de que las columnas necesarias están presentes
    required_columns = ["league_name", "away_team", "home_team"]
    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"La columna {column} es requerida en el archivo CSV.")
    
    # Limpiar los datos
    df["league_name"] = df["league_name"].str.strip().fillna("Unknown")

    df["league_name"] = df["league_name"].astype(str)

    df["league_name"] = df["league_name"].str.lower()

    return df

def populate_database_from_csv_leagues(session, csv_file):
    """
    Puebla la base de datos con los datos del archivo CSV dado.
    """
    df = read_csv_and_transform_leagues(csv_file)

    # Extraer nombres únicos de equipos (países)
    team_names = pd.concat([df["home_team"], df["away_team"]]).unique()

    for index, row in df.iterrows():
        league_name = row["league_name"]
        country_name = row["country_name"]

        # Verificar si la liga ya existe
        league = session.query(League).filter(League.league_name == league_name).first()

        if not league:
            try:
                league = League(league_name=league_name, country_name=country_name)
                session.add(league)
                session.commit()
            except Exception as e:
                print(f"Error al insertar la liga {league_name}: {e}")
                session.rollback()
        else:
            print(f"La liga {league_name} ya existe en la base de datos.")
            
