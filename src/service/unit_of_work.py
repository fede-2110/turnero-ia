# src/service/unit_of_work.py
from contextlib import contextmanager
from app import db

class UnitOfWork:
    @contextmanager
    def start(self):
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
