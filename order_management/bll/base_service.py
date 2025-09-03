from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from dal import BaseDao
from utils import get_logger


class BaseService(ABC):
    """ABC可用作抽象，即被抽象装饰器描述的方法，必须要在子类中实现。"""
    @property
    @abstractmethod
    def service_name(self):
        """要求每个子类都有一个服务名称"""
        pass

    @property
    @abstractmethod
    def model_class(self):
        """要求每个子类对应一个模型（UserService-User）"""
        pass

    def __init__(self):
        """从此之后，所有的service无需再去实例化logger，使用统一的日志记录器"""
        self.logger = get_logger()

    def get_list(self, db: Session):
        """获取所有记录"""
        try:
            result = BaseDao.get_list(db, self.model_class)
            msg = f'{self.service_name}-获取列表成功'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-获取列表失败：{str(e)}'
            self.logger.error(msg)
            return None

    def get_by_id(self, db: Session, pk):
        """根据主键获取记录"""
        try:
            result = BaseDao.get_by_id(db, self.model_class, pk)
            msg = f'{self.service_name}-根据ID[{pk}]获取记录成功'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-根据ID[{pk}]获取记录失败：{str(e)}'
            self.logger.error(msg)
            return None

    def create(self, db: Session, obj):
        """创建新记录"""
        try:
            result = BaseDao.create(db, obj)
            msg = f'{self.service_name}-创建记录成功！'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-创建记录失败：{str(e)}'
            self.logger.error(msg)
            return None

    def update(self, db: Session, db_obj):
        """更新记录"""
        try:
            result = BaseDao.update(db, db_obj)
            msg = f'{self.service_name}-更新记录成功！'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-更新记录失败！原因：{str(e)}'
            self.logger.error(msg)
            return None

    def delete(self, db: Session, db_obj):
        """删除记录"""
        try:
            BaseDao.delete(db, db_obj)
            msg = f'{self.service_name}-删除记录成功！'
            self.logger.info(msg)
            return True
        except Exception as e:
            msg = f'{self.service_name}-删除记录失败！原因：{str(e)}'
            self.logger.error(msg)
            return False

    def get_list_by_condition(self, db: Session, **filters):
        """根据条件获取记录列表"""
        try:
            result = BaseDao.get_list_by_condition(db, self.model_class, **filters)
            msg = f'{self.service_name}-根据条件{filters}获取列表成功'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-根据条件{filters}获取列表失败：{str(e)}'
            self.logger.error(msg)
            return None

    def get_single_by_condition(self, db: Session, **filters):
        """根据条件获取单条记录"""
        try:
            result = BaseDao.get_single_by_condition(db, self.model_class, **filters)
            msg = f'{self.service_name}-根据条件{filters}获取单条记录成功'
            self.logger.info(msg)
            return result
        except Exception as e:
            msg = f'{self.service_name}-根据条件{filters}获取单条记录失败：{str(e)}'
            self.logger.error(msg)
            return None

    def execute_rollback(self, db: Session, e):
        if db and db.is_active:
            db.rollback()
            msg = f'{self.service_name}-执行了回滚操作，错误原因：{e}！'
        else:
            msg = 'session已经关闭，无法回滚！'
        self.logger.error(msg)

    def execute_commit(self, db: Session):
        if db and db.is_active:
            db.commit()
            msg = f'{self.service_name}-执行了提交操作！'
        else:
            msg = 'session已经关闭，无法回滚！'
        self.logger.error(msg)