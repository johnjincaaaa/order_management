from sqlalchemy import and_
from sqlalchemy.orm import Session

class BaseDao:
    """如果只是做基本的数据操作，可以直接使用BaseDao的类方法实现"""

    @classmethod
    def get_list(cls, db: Session, model):
        return db.query(model).all()

    @classmethod
    def create(cls, db: Session, obj):
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @classmethod
    def get_by_id(cls, db: Session, model, pk):
        return db.query(model).get(pk)

    @classmethod
    def update(cls, db: Session, db_obj):
        db.commit()
        db.refresh(db_obj)
        return db_obj

    @classmethod
    def delete(cls, db: Session, db_obj):
        db.delete(db_obj)
        db.commit()

    @classmethod
    def get_list_by_condition(cls, db: Session, model, **filters):
        query = db.query(model)
        for key, value in filters.items():
            query = query.filter(and_(getattr(model, key) == value))
        return query.all()

    @classmethod
    def get_single_by_condition(cls, db: Session, model, **filters):
        query = db.query(model)
        for key, value in filters.items():
            query = query.filter(and_(getattr(model, key) == value))
        return query.first()