import time
import random

from crawlers.setting import Setting
from crawlers.log import Log
from crawlers import JOB_BANK_LIST
from helpers.data_convert_helper import ConvertData


Log()
s = Setting()
df = s.get_csv_from_s3()


class CreativeCoderJobSearch():
    def __init__(self, keyword):
        self.keyword = keyword

    def run(self):
        for JobPlatform in JOB_BANK_LIST:
            job_platform = JobPlatform(self.keyword)
            job_platform.fetch_request(JobPlatform)


if __name__ == '__main__':
    title_keyword_list = df['title_keyword'].tolist()
    title_keyword_list = [x for x in title_keyword_list if x]
    print(title_keyword_list)
    cd = ConvertData()
    cd.readme_init()
    cd.csv_init()
    for keyword in title_keyword_list:
        print(f"You search keywords: {keyword}")
        crawler = CreativeCoderJobSearch(keyword)
        time.sleep(random.randrange(1, 10))
        crawler.run()
    cd.merge_csv()
    cd.csv_to_json()
    cd.json_transform()