import pytest

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.connection import Base
from app.models.user_model import User
from app.models.address_model import Address


@pytest.fixture
def db():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    @event.listens_for(test_engine, "connect")
    def enable_foreign_keys(connection, record):
        cursor = connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )

    Base.metadata.create_all(bind=test_engine)

    session = TestingSessionLocal()

    try:
        session.add(
            User(
                auth_user_id=1001,
                full_name="Test User",
                is_active=True
            )
        )
        session.commit()

        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()
