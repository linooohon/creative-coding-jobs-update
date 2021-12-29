import re
import requests
import pandas as pd
import time
import random
import logging
from urllib.parse import urlencode
# from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from typing import List, Type


from crawlers.setting import Setting
from .base_crawler import BaseCrawler

s = Setting()


class Indeed(BaseCrawler):
    def __init__(self, keyword):
        self.result_list = []
        self.keyword = keyword
        # self.ua = UserAgent()
        self.s3_keyword_df = s.get_csv_from_s3()
        self.platform_name = s.indeed_setting()['platform_name']
        self.platform_url = s.indeed_setting()['platform_url']
        self.query = s.indeed_setting()['query']
        self.referer_list = s.indeed_setting()['referer_list']
        self.ip_list = s.indeed_setting()['ip_list']
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
            "Referer": self.referer_list[random.randrange(0, 25)],
        }

    def get_job_list(self, soup: BeautifulSoup):
        pre = soup.find('div', class_='mosaic-provider-jobcards')
        if not pre:
            return None
        return pre.find_all('a', class_='tapItem')

    def get_job_name(self, job_item: Tag) -> str:
        parent_node = job_item.find('h2', class_='jobTitle')
        if not parent_node.find('span', recursive=False):
            return "None"
        return parent_node.find('span', recursive=False).text

    def get_job_page_link(self, job_item: Tag) -> str:
        return 'https://www.indeed.com' + job_item.get('href')
    
    def get_company_name(self, job_item: Tag) -> str:
        if not job_item.find('span', class_='companyName'):
            return "None"
        elif not job_item.find('span', class_='companyName').find('a'):
            return "None"
        else:
            return job_item.find('span', class_='companyName').find('a').text.strip()

    def get_company_page_link(self, job_item: Tag, company_name, job_name, job_page_link) -> str:
        company_name_tag = job_item.find('a', class_='companyOverviewLink')
        if company_name_tag:
            return 'https://www.indeed.com' + company_name_tag.get('href')
        else:
            logging.warning(
                f"Can't get company page link when processing this job: {company_name}:{job_name}:{job_page_link}")
            return None

    def update_time(self, job_item: Tag) -> str:
        return job_item.find('span', class_='date').text.strip()

    def get_location(self, job_item: Tag) -> str:
        parent_node = job_item.find('div', class_='companyLocation')
        if not parent_node:
            return None
        location = parent_node.text.strip()
        return location

    def filter_skill_get_company_name(self, job_item: Tag) -> list:
        print('start filter')
        filter_company_list = []
        job_page_link = self.get_job_page_link(job_item)
        time.sleep(random.randrange(1, 4))
        resp = requests.get(url=job_page_link,
                            headers=self.headers)
        soup = BeautifulSoup(resp.text, 'html.parser')

        if soup.find('div', class_='icl-u-lg-mr--sm icl-u-xs-mr--xs'):
            company_name = soup.find(
                'div', class_='icl-u-lg-mr--sm icl-u-xs-mr--xs').text
            filter_company_list.append(company_name)
        else:
            return ["No company name", False]

        if soup.find('div', class_='jobsearch-jobDescriptionText'):
            description = soup.find(
                'div', class_='jobsearch-jobDescriptionText').text
        else:
            return [company_name, False]

        skill_keyword_list = self.s3_keyword_df['skill_keyword'].tolist()
        skill_keyword_list = [x for x in skill_keyword_list if x]

        for skill_keyword in skill_keyword_list:
            if skill_keyword in description:
                filter_company_list.append(True)
                return filter_company_list
        filter_company_list.append(False)

        return filter_company_list

    def _insert_to_readme(self, data_list: List[dict], keyword: str, platform_class: Type):
        for i in data_list:
            if not i["company"]:
                data_list.remove(i)
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
        self.query['q'] = self.keyword
        while self.query['start'] < 20:
            # print(self.query['start'])
            page = self.query['start'] // 10
            url = self.platform_url + urlencode(self.query)

            logging.info(f'Now Processing: {url}')
            logging.info(f'Page: {page}, {self.keyword}')
            print(f'Now Processing: {url}')
            print(f'Page: {self.keyword}, {page}')

            resp = requests.get(
                url=url, headers=self.headers)
            soup = BeautifulSoup(resp.text, 'html.parser')

            result = self.get_job_list(soup)

            # 如果沒抓到 job list 頁面就略過這次 url
            if not result:
                logging.error(f'FAIL, no result when crawling this url: {url}')
                logging.info(f'Break here, now go to next loop(next page)')
                self.query['start'] += 10
                continue

            for job_item in result:
                # print(job_item)
                # filter_list = self.filter_skill_get_company_name(job_item)

                # if filter_list[1]:
                job_name = self.get_job_name(job_item)
                job_page_link = self.get_job_page_link(job_item)
                # company_name = filter_list[0]
                # company_page_link = self.get_company_page_link(
                #     job_item, company_name, job_name, job_page_link)
                update_time = self.update_time(job_item)
                location = self.get_location(job_item)
                company_name = self.get_company_name(job_item)
                company_page_link = self.get_company_page_link(job_item, company_name, job_name, job_page_link)
                if company_page_link:
                    company = f'[{company_name}]({company_page_link})'
                else:
                    company = company_name
                    company_page_link = 'None'




                job_dict = {
                    'company': company,
                    'company_name': company_name,
                    'company_page_link': company_page_link,
                    'job': f'[{job_name}]({job_page_link})',
                    'job_name': job_name,
                    'job_page_link': job_page_link,
                    'update_time': update_time,
                    "location": location
                }
                # print(job_dict)
                self.result_list.append(job_dict)
            self.query['start'] += 10
        # print(self.result_list)
        if len(self.result_list) == 0:
            return None
        else:
            logging.info(f'====Finished Processing====: {self.keyword}')
            print(f'====Finished Processing====: {self.keyword}')

            logging.info(f'====Send data to CSV file====: {self.keyword}')
            print(f'====Send data to CSV file====: {self.keyword}')
            self._insert_to_csv(
                self.result_list, self.query['q'], platform_class)
            logging.info(
            f'====Finished Sending data to CSV file====: {self.keyword}')
            print(f'====Finished Sending data to CSV file====: {self.keyword}')

            logging.info(f'====Sending data to readme====: {self.keyword}')
            print(f'====Sending data to readme====: {self.keyword}')
            self._insert_to_readme(
                self.result_list, self.query['q'], platform_class)
            logging.info(
            f'====Finished Sending data to readme====: {self.keyword}')
            print(f'====Finished Sending data to readme====: {self.keyword}')
