from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, declarative_base, sessionmaker

# Declaración de Base para los modelos
Base = declarative_base()


def create_session(database_url="sqlite:///football_data.sqlite"):
    """
    Crea una sesión de base de datos a partir de la URL dada, asegurando que las tablas estén creadas.
    """
    engine = create_engine(database_url, echo=True, future=True)
    # Crear todas las tablas en la base de datos, esto es idempotente
    Base.metadata.create_all(engine)
    session = sessionmaker(autocommit=False, bind=engine)  # TODO: revisar si dejar autoflush=False
    return session()


def add_record(session: Session, record):
    """
    Intenta agregar un registro a la base de datos a través de la sesión dada y maneja las excepciones.
    """
    try:
        session.add(record)
        session.commit()
    except IntegrityError as e:
        print(f"Error al insertar el registro: {e}")
        session.rollback()


# Ejemplo de uso
if __name__ == "__main__":
    # Crear una sesión de la base de datos
    session = create_session()

    # Aquí iría el código para agregar registros utilizando `add_record`
    # Por ejemplo, si tienes un modelo de Match definido en models.py, podrías hacer:
    # new_match = Match(home_team="Team A", away_team="Team B", full_time_home_goals=2)
    # add_record(session, new_match)
