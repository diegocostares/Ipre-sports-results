import os.path as pt
from database import create_session, add_records, process_csv_files
from populate_countries import read_csv_and_transform_countries, populate_database_from_csv_countries
from populate_statistics import read_csv_and_transform_statistics, populate_database_from_csv_statistics
from populate_leagues import read_csv_and_transform_leagues, populate_database_from_csv_leagues
import os


# Ejemplo de uso
def main():
    # Si se desea borrar la base de datos antes de comenzar
    if os.path.exists("football_data.sqlite"):
        os.remove("football_data.sqlite")

    # Crear una sesión de la base de datos
    session = create_session()

    # Leer y transformar los datos del CSV
    # src\database\Fotmob\datos_fotmob_completo.csv
    csv_file = pt.join("src", "database", "Fotmob", "datos_fotmob_completo.csv")

    # Procesar los archivos CSV y poblar la base de datos
    try:
        process_csv_files(session, [csv_file], read_csv_and_transform_countries, populate_database_from_csv_countries)
    except Exception as e:
        print(f"Error al procesar los archivos CSV: {e}")
    finally: 
        # Cerrar la sesión
        session.close()

    # Poblar la base de datos a partir del DataFrame
    #matches = populate_database_from_csv_statistics(csv_file)
    # Agregar el registro a la base de datos
    #for match in matches:
     #   add_record(session, match)
    # Cerrar la sesión


    # Aquí iría el código para agregar registros utilizando `add_record`
    # Por ejemplo, si tienes un modelo de Match definido en models.py, podrías hacer:
    # new_match = Match(home_team="Team A", away_team="Team B", full_time_home_goals=2)
    # add_record(session, new_match)

if __name__ == "__main__":
    main()