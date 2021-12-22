import re
from abc import ABC, abstractmethod

import requests
from bs4 import BeautifulSoup


class BaseCrawler(ABC):
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.data_list = []
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }

    @abstractmethod
    def get_job_list(self):
        return NotImplemented

    # @abstractmethod
    # def get_company_name(self):
    #     return NotImplemented

    @abstractmethod
    def get_company_page_link(self):
        return NotImplemented

    @abstractmethod
    def get_job_name(self):
        return NotImplemented

    @abstractmethod
    def get_job_page_link(self):
        return NotImplemented

    @abstractmethod
    def update_time(self):
        return NotImplemented

    @abstractmethod
    def fetch_request(self):
        return NotImplemented
