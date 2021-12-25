import io
import boto3
import pandas as pd

from dotenv import load_dotenv
from os import environ

# env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True)

class Setting():
    def __init__(self):
        self.AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID')
        self.AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY')
        self.AWS_S3_BUCKET = environ.get('AWS_S3_BUCKET')
        self.AWS_S3_FILE_NAME = environ.get('AWS_S3_FILE_NAME')

        self.BOTO3_SESSION = boto3.Session(
            aws_access_key_id=self.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
        )
        self.S3 = self.BOTO3_SESSION.resource('s3')

    def get_csv_from_s3(self):
        file = self.S3.Object(self.AWS_S3_BUCKET, self.AWS_S3_FILE_NAME).get()['Body'].read()
        df = pd.read_csv(io.BytesIO(file), keep_default_na=False)
        return df

    def indeed_setting(self):
        platform_name = 'indeed'
        platform_url = 'https://www.indeed.com/jobs?'
        query = {
            'q': 'sound design',
            'fromage': '14',
            'ts': '1630833670404',
            'rq': '1',
            'newcount': '97580',
            'rsldx': '0',
            'start': 0
        }
        referer_list = [
            'indeed.zendesk.com/hc/en-gb?redirect=false',
            'indeed.zendesk.com/hc/es?redirect=false',
            'support.indeed.com/hc/en-gb',
            'indeed.zendesk.com/hc/en-us?redirect=false',
            'support.indeed.com/hc/en-ca',
            'support.indeed.com/hc/es',
            'indeed.zendesk.com/hc/de?redirect=false',
            'indeed.zendesk.com/hc/en-ca?redirect=false',
            'es.indeed.com/support/contact',
            'indeed.zendesk.com/hc/tr?redirect=false',
            'ca.indeed.com/support/contact',
            'indeed.zendesk.com/hc/en-nz?redirect=false',
            'uk.indeed.com/support/contact',
            'indeed.zendesk.com/hc/cs?redirect=false',
            'www.indeed.co.uk/support/contact',
            'es.indeed.com/support/contact',
            'indeed.zendesk.com/hc/it?redirect=false',
            'indeed.zendesk.com/hc/es-es?redirect=false',
            'indeed.zendesk.com/hc/ko?redirect=false',
            'indeed.zendesk.com/hc/da?redirect=false',
            'www.indeed.jobs/',
            'www.hiringlab.org/',
            'www.indeedevents.com/',
            'www.indeed.ca/support/contact',
            'www.superspringsinternational.com/users/seodakhoaphuongdo/',
            'indeed.zendesk.com/hc/es-419?redirect=false'
        ]
        ip_list = {
            "http": "116.251.216.95",
            "http": "136.228.141.154",
            "http": "192.168.1.105",
            "http": "192.168.1.103",
            "http": "192.168.1.104"
        }
        indeed_setting_dict = {
            'platform_name': platform_name,
            'platform_url': platform_url,
            'query': query,
            'referer_list': referer_list,
            'ip_list': ip_list
        }
        return indeed_setting_dict

    def linkedIn_setting(self):
        # https://www.linkedin.com/jobs/search/?keywords=creative%20developer
        # https://www.linkedin.com/jobs/search/?keywords=creative%20developer&position=1&pageNum=0
        # https://www.linkedin.com/jobs/search/?keywords=Creative%20Developer&location=United%20States&locationId=&geoId=103644278&sortBy=DD&f_TPR=r2592000&position=1&pageNum=0
        # most recent https://www.linkedin.com/jobs/search/?keywords=Creative%20Developer&location=United%20States&sortBy=DD&f_TPR=r2592000&position=1&pageNum=0
        # most relevant https://www.linkedin.com/jobs/search/?keywords=Creative%20Developer&location=United%20States&sortBy=R&f_TPR=r2592000&position=1&pageNum=0
        # sortBy=R&f_TPR=r2592000
        platform_name = 'linkedIn'
        platform_url = 'https://www.linkedin.com/jobs/search/?'
        query = {
            'keywords': 'sound design',
            'location': 'Worldwide', 
            'sortBy': 'R', # most relevant
            'f_TPR': 'r2592000',  # past month
            # 'start': '0',
            'position': '1',
            'pageNum': '0',
        }
        referer_list = [
            'https://www.linkedin.com/',
            'www.job.com/index.php?m=subscribe',
            'nuxtjs.org/',
            'www.journeyagency.com/',
            'company.sbb.ch/de/medien/medienstelle/medienmitteilungen/detail.html/2020/9/1509-1',
            'neweratech.co.uk/',
            'about.google/products/',
            'www.lotteriescouncil.org.uk/',
            'about.google/',
            'parscoders.com/?ref=12062',
            'www.lightspeedhq.com/',
            'www.brandbucket.com/names/zetyx',
            'www.netohq.com/',
            'www.lightspeedhq.nl/',
            'www.cookieyes.com/',
            'www.namesilo.com/',
            'www.hostinger.com/web-hosting',
            'www.ionos.com/ecommerce-solutions/oscommerce-hosting?ac=OM.US.USo64K403747T7073a',
            'poland.payu.com/',
            'www.liquidityservices.com/privacy-policy/',
            'biurokarier.pwr.edu.pl/pl/polityka-prywatnosci/',
            'www.optimhome.com/',
            'sucuri.net/',
            'sucuri.net/',
            'jp.hach.com/',
            'www.plesk.com/',
            'www.usyazilim.com.tr/',
            'www.showoffimports.nl/brands/141-Car%20Keychains.html',
            'www.powerplay.studio/sk/career/',
            'fintechthon.com/',
            'www.credit-suisse.com/ch/de/privatkunden/konto-karten/viva-kids.html',
            'www.hcsa.org.sg/get-involved/',
            'www.corteva.com/',
            'agentmarketing.com/'
        ]
        ip_list = {
            "http": "116.251.216.95",
            "http": "136.228.141.154",
            "http": "192.168.1.105",
            "http": "192.168.1.103",
            "http": "192.168.1.104"
        }
        linkedIn_setting_dict = {
            'platform_name': platform_name,
            'platform_url': platform_url,
            'query': query,
            'referer_list': referer_list,
            'ip_list': ip_list
        }
        return linkedIn_setting_dict

    def simplyhired_setting(self):
        platform_name = 'simplyhired'
        platform_url = 'https://www.simplyhired.com/search?'
        query = {
            'q': 'sound design',
            'pn': '1',
        }
        referer_list = [
            'https://www.simplyhired.com/',
        ]
        ip_list = {
            "http": "116.251.216.95",
            "http": "136.228.141.154",
            "http": "192.168.1.105",
            "http": "192.168.1.103",
            "http": "192.168.1.104"
        }
        simplyhired_setting_dict = {
            'platform_name': platform_name,
            'platform_url': platform_url,
            'query': query,
            'referer_list': referer_list,
            'ip_list': ip_list
        }
        return simplyhired_setting_dict

    def glassdoor_setting(self):
        platform_name = 'glassdoor'
        platform_url = 'https://www.glassdoor.com/Job/jobs.htm?'
        query = {
            'sc.keyword': 'sound design',
            'fromAge': 14,
        }
        referer_list = [
            'https://www.glassdoor.com/',
        ]
        ip_list = {
            "http": "116.251.216.95",
            "http": "136.228.141.154",
            "http": "192.168.1.105",
            "http": "192.168.1.103",
            "http": "192.168.1.104"
        }
        glassdoor_setting_dict = {
            'platform_name': platform_name,
            'platform_url': platform_url,
            'query': query,
            'referer_list': referer_list,
            'ip_list': ip_list
        }
        return glassdoor_setting_dict
