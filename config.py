from urllib.parse import quote_plus as urlquote

from common.utils import ConfigUtils


class Config(object):
    config = ConfigUtils.get_mysql_config()
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{config["user"]}:{urlquote(config["pass"])}@{config["host"]}:{config["port"]}/{config["db"]}?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
