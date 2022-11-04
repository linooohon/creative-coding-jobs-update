import csv
import json
import subprocess
import pandas as pd
from datetime import datetime
from crawlers.setting_factory import Setting
from crawlers import JOB_BANK_LIST_DAILY, JOB_BANK_LIST_MONDAY

class ConvertData():
    def __init__(self):
        # if datetime.now().weekday() == 0:
            # self.job_bank_list = JOB_BANK_LIST_MONDAY
        # else:
        self.job_bank_list = JOB_BANK_LIST_DAILY
    def readme_init(self):
        for JobPlatform in self.job_bank_list:
            with open(f"./static/readme/readme_{JobPlatform.__name__}.md", "w+") as f:
                f.write("\n")
            markdown_content = f'<h1 style="text-align: center;">Jobs on {JobPlatform.__name__}</h1>'
            with open(f"./static/readme/readme_{JobPlatform.__name__}.md", "a") as f:
                f.write(markdown_content)

    def csv_init(self):
        for JobPlatform in self.job_bank_list:
            with open(f"./static/csv/csv_{JobPlatform.__name__}.csv", "w+") as f:
                f.write("platform,keyword,company,company_name,company_page_link,job,job_name,job_page_link,update_time,location\n")

    def merge_csv(self):
        with open(f"./static/csv/merge.csv", "w+") as f:
            f.write("platform,keyword,company,company_name,company_page_link,job,job_name,job_page_link,update_time,location\n")
        for JobPlatform in self.job_bank_list:
            with open(f"./static/csv/csv_{JobPlatform.__name__}.csv", "r") as in_file, open(f"./static/csv/csv_{JobPlatform.__name__}_stripHeader.csv", "w") as out_file:
                reader = csv.reader(in_file)
                next(reader, None)  # skip the headers
                writer = csv.writer(out_file)
                for row in reader:
                    writer.writerow(row)
        p = subprocess.Popen("sed 1d ./static/csv/*_stripHeader.csv >> ./static/csv/merge.csv", shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
        output, err = p.communicate()
        print(output)
        print('Exit code:', p.returncode)

    def csv_to_json(self):
        jsonList = []
        with open('./static/csv/merge.csv', encoding='utf-8') as csvf: 
            #load csv file data using csv library's dictionary reader
            fieldnames = ("platform", "keyword", "company", "company_name", "company_page_link", "job", "job_name", "job_page_link", "update_time", "location")
            next(csvf) # 把首 row 的 column name 去掉
            csvReader = csv.DictReader(csvf, fieldnames)

            #convert each csv row into python dict
            for i, row in enumerate(csvReader):
                row['index'] = i # 加 index
                #add this python dict to json array
                jsonList.append(row)
    
        #convert python list to JSON String and write to file
        with open('./static/json/merge.json', 'w', encoding='utf-8') as jsonf: 
            jsonString = json.dumps(jsonList, indent=4)
            # print("jsonString:" + jsonString)
            jsonf.write(jsonString)
    
    def json_transform(self):
        with open('./static/json/merge.json', 'r') as read_file:
            data = json.load(read_file)
            result_list = []
        keyword_filter_list = []
        for i in data:
            if i['keyword'] not in keyword_filter_list:
                keyword_filter_list.append(i['keyword'])
                result_list.append({i['keyword']: []})
        # print("first result_list: " + result_list)
        for x in data:
            for i in result_list:
                for j in i:
                    if x['keyword'] == j:
                        i[j].append(x)         
        with open('./static/json/final.json', 'w') as file:
            json.dump(result_list, file)
    
    def final_readme_init(self):
        update_date = datetime.utcnow().date()
        markdown_content = f'<h1 align="center">Creative Coding Jobs Update</h1>'
        with open(f"../README.md", "w+") as f:
            f.write(markdown_content)
        with open(f"../README.md", "a") as f:
            f.write(f'\n<p align="center">Last updated on: {update_date}</p>\n\n## TOC\n\n')
        s = Setting()
        title_keyword_list = s.TITLE_KEYWORD.split(',')
        # df = s.get_csv_from_s3()
        # title_keyword_list = df['title_keyword'].tolist()
        # title_keyword_list = [x for x in title_keyword_list if x]
        with open(f"../README.md", "a") as f:
            for keyword in title_keyword_list:
                keyword_filename = '_'.join(keyword.split())
                f.write(f'\n- <a href="https://github.com/linooohon/creative-coding-jobs-update/blob/main/JOBLIST/{keyword_filename}.md" target="_blank">{keyword}</a>')
    
    def final_json_to_readme(self):
        with open("./static/json/final.json", "r") as read_file:
            data = json.load(read_file)
        for i in data:
            for keyword, value in i.items():
                keyword_filename = '_'.join(keyword.split())
                with open(f"../JOBLIST/{keyword_filename}.md", "w") as f:
                    pass
                df = pd.DataFrame(value).sort_values(["platform"]).reset_index(drop=True)
                columns = ['keyword', 'company_name', 'company_page_link', 'job_name', 'job_page_link', 'index']
                df.drop(columns, inplace=True, axis=1)
                df.index += 1
                markdown_content = "\n"
                # toc_a_link = ''.join(keyword.split())
                # markdown_content += f'\n#### {keyword} <a name="{toc_a_link}" />'
                markdown_content += "\n" + df.to_markdown()
                with open(f"../JOBLIST/{keyword_filename}.md", "a") as f:
                    f.write(markdown_content)