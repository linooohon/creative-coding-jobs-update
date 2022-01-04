import time
import random
import logging
import requests
import pandas as pd
from bs4.element import Tag
from bs4 import BeautifulSoup
from typing import List, Type
from urllib.parse import urlencode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as GoogleService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from .indeed_base import IndeedBase
from crawlers.setting_factory import Setting as S
from crawlers.platform_setting.indeedjp_setting import IndeedJPSetting as IN_JP


class IndeedJP(IndeedBase):
    def __init__(self, keyword):
        self.s = S(IN_JP)
        self.result_list = []
        self.keyword = keyword
        self.s3_keyword_df = self.s.get_csv_from_s3()
        self.platform_name = self.s.platform_name
        self.platform_url = self.s.platform_url
        self.query = self.s.query
        self.query['start'] = 0
        self.referer_list = self.s.referer_list
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
            "Referer": self.referer_list[random.randrange(0, 25)]
        }

    def get_job_page_link(self, job_item: Tag) -> str:
        return 'https://jp.indeed.com' + job_item.get('href')
    
    def get_company_page_link(self, job_item: Tag, company_name, job_name, job_page_link) -> str:
        company_name_tag = job_item.find('a', class_='companyOverviewLink')
        if company_name_tag:
            return 'https://jp.indeed.com' + company_name_tag.get('href')
        else:
            logging.warning(
                f"Can't get company page link when processing this job: {company_name}:{job_name}:{job_page_link}")
            return None