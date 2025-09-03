from bll.base_service import BaseService
from models import Cart


class CartService(BaseService):
    """购物车服务类，没有多余的方法，只有通用方法"""

    @property
    def service_name(self):
        return '购物车管理'

    @property
    def model_class(self):
        return Cart
