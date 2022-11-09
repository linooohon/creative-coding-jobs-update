import time
import random
import subprocess
from typing import Type
from datetime import datetime

from crawlers.setting_factory import Setting
from crawlers.log import Log
from crawlers import JOB_BANK_LIST_DAILY, JOB_BANK_LIST_MONDAY
from crawlers.indeed_jp import IndeedJP
from helpers.data_convert_helper import ConvertData


Log().clean_log()
s = Setting()
# df = s.get_csv_from_s3() # Cancel AWS S3 at 2022/11/04

class CreativeCoderJobSearch():
    def __init__(self, keyword):
        self.keyword = keyword
        # if datetime.now().weekday() == 0:
            # every monday update indeed, indeed uk
            # self.job_bank_list = JOB_BANK_LIST_MONDAY
        # else:
        self.job_bank_list = JOB_BANK_LIST_DAILY

    def run(self):
        for JobPlatform in self.job_bank_list:
            job_platform = JobPlatform(self.keyword)
            job_platform.fetch_request(JobPlatform)
    # def run_selenium(self):
    #     for JobPlatform in JOB_BANK_LIST:
    #         job_platform = JobPlatform(self.keyword)
    #         job_platform.fetch_request(JobPlatform)


class FileHandler():
    def get_keyword(self):
        print('aws bucket', s.AWS_S3_BUCKET)
        print('aws file', s.AWS_S3_FILE_NAME)
        print('keyword', s.TITLE_KEYWORD)
        # title_keyword_list = df['title_keyword'].tolist()
        # title_keyword_list = [x for x in title_keyword_list if x]
        title_keyword_list = s.TITLE_KEYWORD.split(',')
        print(title_keyword_list)
        return title_keyword_list

    def transform(self, cd: Type):
        print("enter merge_csv")
        cd.merge_csv()
        print("enter csv_to_json")
        cd.csv_to_json()
        print("enter json_transform")
        cd.json_transform()
        print("enter final readme init")
        cd.final_readme_init()
        print("finished final readme init")
        cd.final_json_to_readme()
        print("finished final json to readme")


if __name__ == '__main__':
    fh = FileHandler()
    title_keyword_list = fh.get_keyword()
    cd = ConvertData()
    cd.readme_init()
    cd.csv_init()
    for keyword in title_keyword_list:
        print(f"You search keywords: {keyword}")
        crawler = CreativeCoderJobSearch(keyword)
        time.sleep(random.randrange(7, 15))
        crawler.run()
    fh.transform(cd)
    subprocess.Popen('date -u "+DATE: %Y-%m-%d, TIME: %H:%M:%S / UTC+0" > ./log/update_time.log', shell=True)
    # with open("./static/txt/indeed_jp_keyword.txt", "r") as f:
    #     gen = (i.strip('\n') for i in f.readlines())
    #     for keyword in gen:
    #         print(f"You search keywords: {keyword}")
    #         crawler = CreativeCoderJobSearch(keyword)
    #         time.sleep(random.randrange(10, 30))
    #         crawler.run()
