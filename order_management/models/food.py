from sqlalchemy import Column, Integer, String, DECIMAL
from models.base import Base


class Food(Base):
    __tablename__ = 't_food'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(8, 2), nullable=False)
    specs = Column(String(20), nullable=False)
    status = Column(Integer, default=1, nullable=False)
