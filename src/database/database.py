from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base, sessionmaker
import pandas as pd
import os.path as pt

from populate_statistics import read_csv_and_transform_statistics, populate_database_from_csv_statistics
from populate_countries import read_csv_and_transform_countries, populate_database_from_csv_countries

from models import Base

# Declaración de Base para los modelos


def create_session(database_url="sqlite:///football_data.sqlite"):
    """
    Crea una sesión de base de datos a partir de la URL dada, asegurando que las tablas estén creadas.
    """
    engine = create_engine(database_url, echo=True, future=True)
    # Crear todas las tablas en la base de datos, esto es idempotente
    Base.metadata.create_all(engine)
    session = sessionmaker(autocommit=False, bind=engine, autoflush=False)  # TODO: revisar si dejar autoflush=False
    return session()


def add_records(session: Session, records):
    """
    Intenta agregar un registro a la base de datos a través de la sesión dada y maneja las excepciones.
    """
    try:
        session.add_all(records)
        session.commit()
    except IntegrityError as e:
        print(f"Error al insertar el registro: {e}")
        session.rollback()

def process_csv_files(session, csv_files, read_func, populate_func):
    for csv_file in csv_files:
        if pt.exists(csv_file):
            print(f"Procesando {csv_file}")
            read_func(csv_file)
            populate_func(session, csv_file)
        else:
            print(f"Archivo no encontrado: {csv_file}")


