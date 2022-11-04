import requests
import pandas as pd
import random
import logging
import time
from urllib.parse import urlencode
# from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from bs4.element import Tag
from typing import List
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as GoogleService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


from crawlers.setting_factory import Setting
from .base_crawler import BaseCrawler

s = Setting()

class LinkedIn(BaseCrawler):
    def __init__(self, keyword):
        self.result_list = []
        self.keyword = keyword
        # self.ua = UserAgent()
        # self.s3_keyword_df = s.get_csv_from_s3()
        self.platform_name = s.linkedIn_setting()['platform_name']
        self.platform_url = s.linkedIn_setting()['platform_url']
        self.query = s.linkedIn_setting()['query']
        self.referer_list = s.linkedIn_setting()['referer_list']
        # self.headers = {
        #     "User-Agent": self.ua.random,
        # }

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

        with open(f"./static/readme/readme_{platform_class.__name__}.md", "a") as f:
            f.write(markdown_content)
    
    def _insert_to_csv(self, data_list: List[dict], keyword: str, platform_class):
        df = pd.DataFrame(data_list).sort_values(
            ["company"]).reset_index(drop=True)
        df.insert(0, 'platform', platform_class.__name__)
        df.insert(1, 'keyword', keyword)
        df.index += 1
        csv_content = df.to_csv(index=False, header=None)
        with open(f"./static/csv/csv_{platform_class.__name__}.csv", "a") as f:
            f.write(csv_content)

    def fetch_request_2(self, platform_class):
        self.query['keywords'] = self.keyword
        # while self.query['start'] < 30:
        url = self.platform_url + urlencode(self.query)
        print(url)

        logging.info(f'Now Processing: {url}')
        # logging.info(f'Page: {page}, {self.keyword}')
        print(f'Now Processing: {url}')
        # print(f'Page: {self.keyword}, {page}')

        # resp = requests.get(
        #     url=url, headers=self.headers)

        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            # "cookie": 'bcookie="v=2&f50620a6-1d27-43ef-8c82-889eb4d9ab7a"; _ga=GA1.2.1567656659.1626282027; bscookie="v=1&20210714170037e2cf71dc-e5fd-4cea-88d7-a5d2285b4cbeAQEdGelxaHqgpnZatX3Ln0xvi-c4Nae4"; li_rm=AQE_xAkP-aDnpAAAAXql9qYGtkgPo4SJejsW5Sr5AOXMwk58W71IubWozwOBB3GMxnCAQBiLR1sAghsksUhnL36G73rBjEt222NC2SPpt_qGkSANTqc48bo5fbOOgRS5liTvBNEu1M6F0ITkqhSaPFHaSFDzGISHYwNXpc-jMZNHAzZvSVjV6LpiE6bOTXsLwSrqF6IGFiOHns6orVPtJXwVlYfvXo_HEzREsnpe0g9QlU3pZwBHtplvj_4X17A6hHwGoGdcHX3JaSylY3hebh7gOLzALVMi_rJ1c5zRpA1-l67E2F31QGMsJbejCMZquwTeTcr-YaULXM1zXwo; _gcl_au=1.1.384073379.1626411391; G_ENABLED_IDPS=google; visit=v=1&M; g_state={"i_p":1632621074798,"i_l":3}; liap=true; JSESSIONID="ajax:5358018358150210109"; liveagent_oref=https://www.linkedin.com/help/lms/answer/a424393; liveagent_vc=2; liveagent_ptid=eea97cca-9bb3-4667-97d8-9230e77018fe; li_theme=light; mbox=session#ba7ee320771b4a1989c41e0b722fc50a#1636783710|PC#ba7ee320771b4a1989c41e0b722fc50a.32_0#1652333860; lang=v=2&lang=en-us; li_at=AQEDASfccHYBwZRIAAABe_1vbK8AAAF9-dW5404AC--U_lAJn26zRKOr3ruder-ZxQpcQxfQY_sAIrzxiGd8ExDdF3hOEQOvmPqZnifiAT0M9_mYlwZWd3BrIV0cLLGCINoMv0DaeqnlcMgKPFtuAdAF; timezone=Asia/Taipei; li_theme_set=user; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; aam_uuid=85944933508547408802946978665592763967; lil-lang=en_US; gpv_pn=www.linkedin.com%2Flearning%2Flearning-github-actions-2; s_tp=2622; s_cc=true; s_plt=2.31; s_pltp=www.linkedin.com%2Flearning%2Flearning-github-actions-2; s_tslv=1640365531204; s_ips=985; s_ppv=www.linkedin.com%2Flearning%2Flearning-github-actions-2%2C61%2C38%2C1597%2C1%2C2; lidc="b=OB34:s=O:r=O:a=O:p=O:g=3150:u=337:x=1:i=1640410712:t=1640489403:v=2:sig=AQHg8_xUASjUvYqfMGiafwQTg7vHnrCn"; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C18987%7CMCMID%7C86139535201259828112894383302137693684%7CMCAAMLH-1641015515%7C11%7CMCAAMB-1641015515%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1640417915s%7CNONE%7CMCCIDH%7C193992886%7CvVersion%7C5.1.1; UserMatchHistory=AQJ6exgvI7sXfgAAAX3wHIA-tz1jEhePYh08DnX54oJMUhEPWtqmL3eY6PG4Q9g1wOQPCMXhrqjFQdZGOzKZQDZ_8IyMkZjID4C4qG_606h_qHKDbOlF6gicP4vbme8METyPzONONqGi2Fm95Nhh4xzjLtrNVHzcO7m9NuCFNWmP0gblfWWUSm9_eWka485aQG9uu0o1KYdToD-ddvwVdcHfK0c4JhCD3UI_sur0p4s3EYdfeAX8r9btgVfreUcc9uedyjvYcQ',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36 Edg/95.0.1020.44",
            "referer": self.referer_list[random.randrange(0, len(self.referer_list) - 1)]
        }
        resp = requests.get(url=url, headers=headers)
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


    def fetch_request(self, platform_class):
        self.query['keywords'] = self.keyword
        url = self.platform_url + urlencode(self.query)
        logging.info(f'Now Processing: {url}')
        print(f'Now Processing: {url}')

        s = GoogleService(ChromeDriverManager().install())
        opts = webdriver.ChromeOptions()
        opts.add_argument("--incognito")
        opts.headless = True
        browser = webdriver.Chrome(service=s, options=opts)
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "html.parser")
        result = self.get_job_list(soup)
        # 如果沒抓到 job list 頁面就略過這次 url
        if not result:
            logging.error(f'FAIL, no result when crawling this url: {url}')
            logging.info(f'Break here, now go to next loop(next page)')
            return None
        for job_item in result:
            job_name = self.get_job_name(job_item)
            job_page_link = self.get_job_page_link(job_item)
            company_name = self.get_company_name(job_item)
            company_page_link = self.get_company_page_link(job_item)
            update_time = self.update_time(job_item)
            location = self.get_location(job_item)
            print('=================')
            print('-----------------')

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
            self.result_list.append(job_dict)

        logging.info(f'====Finished Processing====: {self.keyword}')
        print(f'====Finished Processing====: {self.keyword}')

        logging.info(f'====Sending data to CSV file====: {self.keyword}')
        print(f'====Sending data to CSV file====: {self.keyword}')
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
        browser.quit()
        s.stop()
        time.sleep(2)








