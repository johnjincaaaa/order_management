from bll.base_service import BaseService
from models.order import Order, RefundApplication


class OrderService(BaseService):
    """购物车服务类，没有多余的方法，只有通用方法"""

    @property
    def service_name(self):
        return '订单管理'

    @property
    def model_class(self):
        return Order


class RefundService(BaseService):

    @property
    def service_name(self):
        return '退款申请管理'

    @property
    def model_class(self):
        return RefundApplication