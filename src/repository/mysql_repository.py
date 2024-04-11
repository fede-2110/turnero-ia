from src.repository.repository_interface import IRepository
from datetime import datetime, timezone
from app import db

class MysqlRepository(IRepository):
    def __init__(self, model):
        self.model = model

    def add(self, entity):
        db.session.add(entity)

    def get_by_id(self, id):
        return db.session.query(self.model).filter_by(id=id, FechaBaja=None).first()
    
    def get_all(self):
        return db.session.query(self.model).filter(FechaBaja=None).all()

    def update(self, entity):
        db.session.merge(entity)

    def delete(self, entity):
        # Actualiza FechaBaja en lugar de eliminar el registro físicamente
        if entity:
            entity.FechaBaja = datetime.now(timezone.utc)
            db.session.add(entity)
            
    def get_by_query(self, query):
        return db.session.execute(query).all()