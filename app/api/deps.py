from app.db.session import SessionLocal


def get_db():
    # Placeholder for database connection logic
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()