from bll.base_service import BaseService
from models import Food


class FoodService(BaseService):
    """菜品服务类，没有多余的方法，只有通用方法"""

    @property
    def service_name(self):
        return '菜品管理'

    @property
    def model_class(self):
        return Food