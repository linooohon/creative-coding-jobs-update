import re
import logging
import requests
import pandas as pd
from typing import List
from bs4.element import Tag
from bs4 import BeautifulSoup
from urllib.parse import urlencode

from .base_crawler import BaseCrawler
from crawlers.setting_factory import Setting as S
from crawlers.platform_setting.glassdoor_setting import GlassDoorSetting as GD

class Glassdoor(BaseCrawler):
    def __init__(self, keyword):
        self.s = S(GD)
        self.result_list = []
        self.keyword = keyword
        self.s3_keyword_df = self.s.get_csv_from_s3()
        self.platform_name = self.s.platform_name
        self.platform_url = self.s.platform_url
        self.query = self.s.query
        self.referer_list = self.s.referer_list
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44"
        }

    def get_job_list(self, soup: BeautifulSoup):
        pre = soup.find('ul', {'class': ['job-search-key-kgm6qi', 'exy0tjh1']})
        if not pre:
            return None
        return pre.find_all('li', {"class": ["react-job-listing", "eigr9kq0"]})

    def get_job_name(self, job_item):
        node = job_item.find('a', class_="eigr9kq1")
        if not node:
            return None
        job_name = node.find('span').text.strip()
        # \w: 數字、字母、底線
        # \W: 非 \w
        print(job_name)
        job_name_strip = re.sub(r'[\W]', ' ', job_name)  # 這裡是去除所有非\w 的: 是為了去除 "|"，所以使用 \W, 也可以使用 ^\w
        return job_name_strip

    def get_job_page_link(self, job_item: Tag) -> str:
        node = job_item.find(
            'a', {"class": ["jobLink", "eigr9kq1"]})
        if not node:
            return None
        return 'https://www.glassdoor.com' + node.get('href')

    def get_company_name(self, job_item: Tag) -> str:
        node = job_item.find('a', class_="e1n63ojh0")
        if not node:
            return None
        company_name = node.find('span').text.strip()
        company_name_strip = re.sub(r'[\W]', ' ', company_name)
        return company_name_strip

    def get_company_page_link(self):
        return None

    def update_time(self, job_item: Tag) -> str:
        node = job_item.find(
            'div', {"class": ["pl-std", "css-17n8uzw"]})
        if not node:
            return "Recently"
        return node.text.strip()

    def get_location(self, job_item: Tag) -> str:
        node = job_item.find(
            'span', {"class": ["job-search-key-iii9i8", "e1rrn5ka4"]})
        if not node:
            return None
        return node.text.strip()

    def _insert_to_readme(self, data_list: List[dict], keyword: str, platform_class):
        df = pd.DataFrame(data_list).sort_values(
            ["company"]).reset_index(drop=True)
        df.index += 1
        markdown_content = "\n"
        markdown_content += f"\n#### {keyword}"
        markdown_content += "\n" + df.to_markdown()

        with open(f"./readme_{platform_class.__name__}.md", "a") as f:
            f.write(markdown_content)

    def _insert_to_csv(self, data_list: List[dict], keyword: str, platform_class):
        df = pd.DataFrame(data_list).sort_values(
            ["company"]).reset_index(drop=True)
        df.insert(0, 'platform', platform_class.__name__)
        df.insert(1, 'keyword', keyword)
        df.index += 1
        csv_content = df.to_csv(index=False, header=None)
        with open(f"./csv_{platform_class.__name__}.csv", "a") as f:
            f.write(csv_content)

    def fetch_request(self, platform_class):
        self.query['sc.keyword'] = self.keyword
        url = self.platform_url + urlencode(self.query)
        print(url)

        logging.info(f'Now Processing: {url}')
        print(f'Now Processing: {url}')

        resp = requests.get(
            url=url, headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        result = self.get_job_list(soup)

        # 如果沒抓到 job list 頁面就略過這次 url
        if not result:
            logging.error(f'FAIL, no result when crawling this url: {url}')
            logging.info(f'Break here, now go to next loop(next page)')
            return None
        for job_item in result:
            # print(job_item)
            job_name = self.get_job_name(job_item)
            job_page_link = self.get_job_page_link(job_item)
            company_name = self.get_company_name(job_item)
            # company_page_link = self.get_company_page_link(job_item)
            update_time = self.update_time(job_item)
            location = self.get_location(job_item)

            job_dict = {
                'company': company_name,
                'company_name': company_name,
                'company_page_link': 'None',
                'job': f'[{job_name}]({job_page_link})',
                'job_name': job_name,
                'job_page_link': job_page_link,
                'update_time': update_time,
                'location': location,
            }
            # print(job_dict)
            self.result_list.append(job_dict)

        logging.info(f'====Finished Processing====: {self.keyword}')
        print(f'====Finished Processing====: {self.keyword}')

        logging.info(f'====Sending data to CSV file====: {self.keyword}')
        print(f'====Sending data to CSV file====: {self.keyword}')
        self._insert_to_csv(self.result_list, self.query['sc.keyword'], platform_class)
        logging.info(
            f'====Finished Sending data to CSV file====: {self.keyword}')
        print(f'====Finished Sending data to CSV file====: {self.keyword}')

        logging.info(f'====Sending data to readme====: {self.keyword}')
        print(f'====Sending data to readme====: {self.keyword}')
        self._insert_to_readme(
            self.result_list, self.query['sc.keyword'], platform_class)
        logging.info(
            f'====Finished Sending data to readme====: {self.keyword}')
        print(f'====Finished Sending data to readme====: {self.keyword}')
