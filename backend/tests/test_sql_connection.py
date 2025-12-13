from database.database import get_db
from sqlalchemy import text

def test_connection():
    db = next(get_db())
    assert db.execute(text("SELECT 1")).scalar() == 1
