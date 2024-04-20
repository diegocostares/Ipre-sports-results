from datetime import datetime

import pytest
from sqlalchemy.orm import Session

from src.database.database import Base, create_session
from src.database.models import Statistics


@pytest.fixture(scope="module")
def test_engine():
    """Crea un motor SQLAlchemy que apunta a una base de datos en memoria."""
    from sqlalchemy import create_engine

    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="module")
def test_session(test_engine):
    """Crea una sesión para interactuar con la base de datos de prueba."""
    Base.metadata.create_all(test_engine)
    from sqlalchemy.orm import sessionmaker

    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.close()


def test_create_statistics_table(test_session):
    """Test para verificar que la tabla 'statistics' se crea con las columnas correctas."""
    date_str = "2023-04-14"
    time_str = "15:00"
    date = datetime.strptime(date_str, "%Y-%m-%d").date()
    kick_off_time = datetime.strptime(time_str, "%H:%M").time()

    statistics = Statistics(
        statistics_date=date,
        kick_off_time=kick_off_time,
        home_team_name="Team A",
        away_team_name="Team B",
        full_time_home_goals=2,
        full_time_away_goals=1,
        full_time_result="H",
    )
    test_session.add(statistics)
    test_session.commit()

    retrieved_statistics = test_session.query(Statistics).one()
    assert retrieved_statistics.date == date
    assert retrieved_statistics.kick_off_time == kick_off_time
