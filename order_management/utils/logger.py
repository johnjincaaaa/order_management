import logging

from configs.log_config import LOG_CONFIG


class SingletonLogger:
    """我先放这里，后面快速改掉！"""
    _instance = None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # 创建了一个日志对象
            logger_instance = logging.getLogger()
            # 设置了日志对象最大的展示级别为DEBUG
            # 从大到小：DEBUG-调试 INFO-正常消息 WARING-警告 ERROR-错误 CRITICAL-严重错误
            logger_instance.setLevel(LOG_CONFIG['log_level'])
            # 输出器（输出到文件），输出到控制台的输出器，这里不用
            file_handler = logging.FileHandler(LOG_CONFIG['log_file'], encoding=LOG_CONFIG['encoding'])
            # 输出器的日志级别，在日志最大级别的限制下，输出器可以自由规定级别
            file_handler.setLevel(LOG_CONFIG['file_handler_level'])
            # 日志的格式
            formatter = logging.Formatter(LOG_CONFIG['log_format'])
            # 将格式应用到输出器
            file_handler.setFormatter(formatter)
            # 将输出器绑定到日志对象
            logger_instance.addHandler(file_handler)
            cls._instance = logger_instance
        return cls._instance

def get_logger():
    return SingletonLogger()
