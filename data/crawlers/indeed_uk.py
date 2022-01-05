import random
import logging
from bs4.element import Tag

from .indeed_base import IndeedBase
from crawlers.setting_factory import Setting as S
from crawlers.platform_setting.indeeduk_setting import IndeedUKSetting as IN_UK


class IndeedUK(IndeedBase):
    def __init__(self, keyword):
        self.s = S(IN_UK)
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
        return 'https://uk.indeed.com' + job_item.get('href')
    
    def get_company_page_link(self, job_item: Tag, company_name, job_name, job_page_link) -> str:
        company_name_tag = job_item.find('a', class_='companyOverviewLink')
        if company_name_tag:
            return 'https://uk.indeed.com' + company_name_tag.get('href')
        else:
            logging.warning(
                f"Can't get company page link when processing this job: {company_name}:{job_name}:{job_page_link}")
            return None