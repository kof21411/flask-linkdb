import json

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from common.constants import GLOBAL_PATH


class Utils:
    @staticmethod
    def read_file2json(path):
        try:
            with open(path, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            return None

    @staticmethod
    def check_url(url):
        try:
            ua = UserAgent(verify_ssl=False, path="data/0.1.11.json")
            req = requests.get(url, headers={"User-Agent": ua.random},
                               timeout=5)
            req.encoding = "utf-8"
            return req.status_code, req.text
        except Exception as e:
            print(e)
            return None, None

    @staticmethod
    def get_web_title(html):
        try:
            soup = BeautifulSoup(html, 'lxml')
            if soup.title.text and len(soup.title.text) > 0:
                return soup.title.text
        except:
            return "无标题"


class ConfigUtils:
    @staticmethod
    def get_web_config():
        return Utils.read_file2json(GLOBAL_PATH.CONFIG_PATH).get("web", None)

    @staticmethod
    def get_mysql_config():
        return Utils.read_file2json(GLOBAL_PATH.CONFIG_PATH).get("mysql", None)
