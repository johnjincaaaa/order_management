from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DECIMAL, PrimaryKeyConstraint, Index, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from models.base import Base


class Cart(Base):
    """ 购物车 """
    __tablename__ = 't_cart'

    food_id = Column(Integer, ForeignKey('t_food.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('t_user.id'), nullable=False)
    amount = Column(DECIMAL(8, 2), default=0.00, nullable=False)
    subtotal = Column(DECIMAL(8, 2), default=0.00, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('food_id', 'user_id'),
        Index('idx_cart_food', 'food_id'),
        Index('idx_cart_user', 'user_id'),
    )

    food = relationship("Food", backref="carts")


class Order(Base):
    """ 订单主体 """
    __tablename__ = 't_order'

    order_no = Column(String(10), primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('t_user.id'), nullable=False)
    order_person = Column(String(50))
    order_phone = Column(String(50))
    order_address = Column(Text())
    sum_price = Column(DECIMAL(8, 2), default=0.00)
    status = Column(Integer, default=0)
    create_at = Column(TIMESTAMP, default=datetime.now, nullable=False)
    update_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)

    order_details = relationship("OrderDetails", backref="order", cascade="all, delete-orphan")
    refund_applications = relationship("RefundApplication", backref="order", cascade="all, delete-orphan")


class OrderDetails(Base):
    """ 订单详情 """
    __tablename__ = 't_order_details'

    order_no = Column(String(10), ForeignKey('t_order.order_no'), nullable=False)
    food_id = Column(Integer, ForeignKey('t_food.id'), nullable=False)
    amount = Column(DECIMAL(8, 2), nullable=False)
    subtotal = Column(DECIMAL(8, 2), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('order_no', 'food_id'),
    )

    food = relationship("Food", backref="order_details")


class RefundApplication(Base):
    """ 退款申请 """
    __tablename__ = 't_refund_application'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_no = Column(String(10), ForeignKey('t_order.order_no'), nullable=False)
    user_id = Column(Integer, ForeignKey('t_user.id'), nullable=False)
    refund_reason = Column(Text())
    refund_response = Column(Text())
    refund_amount = Column(DECIMAL(8, 2), nullable=False)
    status = Column(Integer, nullable=False)
    create_at = Column(TIMESTAMP, default=datetime.now, nullable=False)
    update_at = Column(TIMESTAMP, default=datetime.now, onupdate=datetime.now, nullable=False)