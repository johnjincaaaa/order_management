from datetime import datetime

from sqlalchemy import Column, Integer, DECIMAL, String, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    balance = Column(DECIMAL(8, 2), default=0.00, nullable=False)
    status = Column(Integer, default=1, nullable=False)
    role = Column(Integer, default=1, nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.now, nullable=False)
    update_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)

    # 用户下的购物车信息
    carts = relationship('Cart', backref='user')
    # 用户拥有的订单信息
    orders = relationship("Order", backref="user", cascade="all, delete-orphan")
    # 用户对应的退款申请单
    refund_applications = relationship("RefundApplication", backref="user", cascade="all, delete-orphan")