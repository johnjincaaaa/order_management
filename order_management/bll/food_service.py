"""
业务逻辑层：
    1、负责业务功能的实现，每个函数都需要完成一个功能主体
    2、负责日志记录
    3、有事务的话，还需要负责事务管理
"""
from ..configs.log_config import get_logger
from ..dal.base_dal import BaseDao
from ..dal.session_manager import SessionManager
from ..models import Food

logger = get_logger()

def get_foods():
    """获取全部食物"""
    try:
        session = SessionManager.get_session()
        foods = BaseDao.get_list(session, Food)
        logger.info('调用get_logs成功！')
        return foods
    except Exception as e:
        # 因为我们本身是控制台程序，因此不能让这样的报错信息影响到界面，所以会使用一个日志库，来记录日志（文件）
        logger.error(e)
        return []
