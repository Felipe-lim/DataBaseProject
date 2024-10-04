def get_db(SessionLocal):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
