import re
import requests
import pandas as pd
import time
import random
import logging
from urllib.parse import urlencode
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from typing import List


from crawlers.setting import Setting
from .base_crawler import BaseCrawler

s = Setting()


class LinkedIn(BaseCrawler):
    def __init__(self, keyword):
        self.result_list = []
        self.keyword = keyword
        self.ua = UserAgent()
        self.s3_keyword_df = s.get_csv_from_s3()
        self.platform_name = s.linkedIn_setting()['platform_name']
        self.platform_url = s.linkedIn_setting()['platform_url']
        self.query = s.linkedIn_setting()['query']
        self.referer_list = s.linkedIn_setting()['referer_list']
        self.ip_list = s.linkedIn_setting()['ip_list']
        self.headers = {
            "User-Agent": self.ua.random,
        }

    def get_job_list(self, soup: BeautifulSoup):
        pre = soup.find('ul', class_='jobs-search__results-list')
        # print(pre)
        if not pre:
            return None
        return pre.find_all('div', class_='base-card')

    def get_job_name(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='base-search-card__info')
        if not parent_node:
            return None
        return parent_node.find('h3', class_='base-search-card__title').text.strip()

    def get_job_page_link(self, job_item: Tag) -> str:
        job_link = job_item.find(
            'a', class_='base-card__full-link').get('href')
        return job_link.strip()

    def get_company_page_link(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='base-search-card__info')
        if not parent_node:
            return None
        pre_node = parent_node.find('h4', class_='base-search-card__subtitle')
        company_link = pre_node.find(
            'a', class_='hidden-nested-link').get('href')
        return company_link.strip()

    def get_company_name(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='base-search-card__info')
        if not parent_node:
            return None
        pre_node = parent_node.find('h4', class_='base-search-card__subtitle')
        company_name = pre_node.find('a', class_='hidden-nested-link').text
        return company_name.strip()

    def update_time(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='base-search-card__metadata')
        print(parent_node)
        if not parent_node:
            return None
        update_time_node = parent_node.find(
            'time', class_='job-search-card__listdate')
        if not update_time_node:
            return None
        update_time = update_time_node.text
        return update_time.strip()

    def get_location(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='base-search-card__metadata')
        if not parent_node:
            return None
        location = parent_node.find(
            'span', class_='job-search-card__location').text
        return location.strip()

    def filter_skill_get_company_name(self, job_item: Tag) -> list:
        return None

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
        self.query['keywords'] = self.keyword
        # while self.query['start'] < 30:
        url = self.platform_url + urlencode(self.query)
        print(url)

        logging.info(f'Now Processing: {url}')
        # logging.info(f'Page: {page}, {self.keyword}')
        print(f'Now Processing: {url}')
        # print(f'Page: {self.keyword}, {page}')

        resp = requests.get(
            url=url, headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # print(soup)

        result = self.get_job_list(soup)
        # print(result)

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
            company_page_link = self.get_company_page_link(job_item)
            update_time = self.update_time(job_item)
            location = self.get_location(job_item)
            print('=================')
            # print(job_name, job_page_link)
            print('-----------------')
            # print(company_name, company_page_link, update_time, location)

            job_dict = {
                'company': f'[{company_name}]({company_page_link})',
                'company_name': company_name,
                'company_page_link': company_page_link,
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

        df = pd.DataFrame(self.result_list)
        logging.info(f'====Sending data to CSV file====: {self.keyword}')
        print(f'====Sending data to CSV file====: {self.keyword}')
        # df.to_csv('linkedin.csv')
        self._insert_to_csv(self.result_list, self.query['keywords'], platform_class)
        logging.info(
            f'====Finished Sending data to CSV file====: {self.keyword}')
        print(f'====Finished Sending data to CSV file====: {self.keyword}')

        logging.info(f'====Sending data to readme====: {self.keyword}')
        print(f'====Sending data to readme====: {self.keyword}')
        self._insert_to_readme(
            self.result_list, self.query['keywords'], platform_class)
        logging.info(
            f'====Finished Sending data to readme====: {self.keyword}')
        print(f'====Finished Sending data to readme====: {self.keyword}')
