import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base

@pytest.fixture(scope="function")
def db_session():
    
    engine = create_engine("sqlite:///:memory:", echo=False)
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db  
    finally:
        db.close()
