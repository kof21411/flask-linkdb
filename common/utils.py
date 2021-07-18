import json

from app import app
from common.constants import GLOBAL_PATH


class Utils:
    @staticmethod
    def read_file2json(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            app.logger.error(e)


class ConfigUtils:
    @staticmethod
    def get_web_config():
        return Utils.read_file2json(GLOBAL_PATH.CONFIG_PATH).get("web", None)
