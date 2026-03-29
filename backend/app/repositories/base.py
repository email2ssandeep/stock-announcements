from sqlalchemy.orm import Session


class BaseRepository:
    def __init__(self, model, db: Session):
        self.model = model
        self.db = db

    def get_all(self):
        return self.db.query(self.model).all()

    def get_by_id(self, record_id: int):
        return self.db.query(self.model).filter(self.model.id == record_id).first()

    def add(self, obj):
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def delete_all(self):
        self.db.query(self.model).delete()
        self.db.commit()
