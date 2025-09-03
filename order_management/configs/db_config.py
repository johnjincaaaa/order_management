"""数据库的配置文件"""
DB_CONFIG = {
    'host': '192.168.132.128',  # 这里需要填入你的ip  192.168.159.129
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'learn5',
    'driver': 'pymysql',
    'charset': 'utf8mb4',
    'pool_size': 5,
    'max_overflow': 10,
    'echo_sql': False
}

def get_connect_string():
    cfg = DB_CONFIG
    return f"mysql+{cfg['driver']}://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}?charset={cfg['charset']}"