import pandas as pd
from typing import List, Type
from abc import ABC, abstractmethod


class BaseCrawler(ABC):
    def __init__(self, keyword: str):
        self.keyword = keyword
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36"
        }

    @abstractmethod
    def get_job_list(self):
        return NotImplemented

    @abstractmethod
    def get_company_page_link(self):
        return NotImplemented
    
    @abstractmethod
    def get_company_name(self):
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
    def get_location(self):
        return NotImplemented

    @abstractmethod
    def fetch_request(self):
        return NotImplemented

    def _insert_to_readme(self, data_list: List[dict], keyword: str, platform_class: Type):
        df = pd.DataFrame(data_list).sort_values(["company"]).reset_index(drop=True)
        df.index += 1
        markdown_content = "\n"
        markdown_content += f"\n#### {keyword}"
        markdown_content += "\n" + df.to_markdown()

        with open(f"./static/readme/readme_{platform_class.__name__}.md", "a") as f:
            f.write(markdown_content)

    def _insert_to_csv(self, data_list: List[dict], keyword: str, platform_class: Type):
        df = pd.DataFrame(data_list).sort_values(
        ["company"]).reset_index(drop=True)
        df.insert(0, 'platform', platform_class.__name__)
        df.insert(1, 'keyword', keyword)
        df.index += 1
        csv_content = df.to_csv(index=False, header=None)
        with open(f"./static/csv/csv_{platform_class.__name__}.csv", "a") as f:
            f.write(csv_content)
