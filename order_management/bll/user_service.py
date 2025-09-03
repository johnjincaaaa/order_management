from .base_service import BaseService
from models import User
from utils import get_logger
from utils.constants import USER_STATUS_FREEZE

logger = get_logger()

class LoginManager:
    """对已登录用户进行管理"""
    _instance = None

    def __init__(self):
        self._current_user_id = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = LoginManager()
        return cls._instance

    @property
    def current_user_id(self):
        return self._current_user_id

    @property
    def is_logged_in(self):
        return self._current_user_id is not None

    def rush(self, user_id):
        self._current_user_id = user_id

    def logout(self):
        if self.is_logged_in:
            self._current_user_id = None

    def require_login(self) -> bool:
        if not self.is_logged_in:
            return False
        return True

class UserService(BaseService):

    @property
    def service_name(self):
        return '用户服务'

    @property
    def model_class(self):
        return User


    def login_check(self, session, username, password, role):
        try:
            user = self.get_single_by_condition(
                session,
                username=username
            )
            if not user:
                msg = '用户不存在！'
            elif user.password != password:
                msg = '账号密码不匹配！'
            elif user.status == USER_STATUS_FREEZE:
                msg = f'用户 {username} 已被冻结！'
            elif user.role != role:
                msg = '用户与角色不匹配！'
            else:
                msg = f'用户 {username} 登录成功！'
                login_manager.rush(user.id)
                return True, msg
            return False, msg
        except Exception as e:
            msg = f'login_check调用失败：原因{str(e)}'
            logger.error(msg)
            return False, '登录错误，请查看后台日志'

login_manager = LoginManager()
