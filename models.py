# 数据库配置
from config import Config

DATABASE = {
    'engine': 'mysql',  # support mysql,postgresql in the future
    'name': Config.mysql_name,
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'lpj020134'
}
