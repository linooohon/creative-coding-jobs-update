from .base_setting import BaseSetting

class IndeedUKSetting(BaseSetting):
    # https://jp.indeed.com/jobs?q=frontend%20engineer&l=
    platform_name = 'indeed_uk'
    platform_url = 'https://uk.indeed.com/jobs?'
    query = {
        'q': 'sound design',
        # 'fromage': '14',
        # 'ts': '1630833670404',
        # 'rq': '1',
        # 'newcount': '97580',
        # 'rsldx': '0',
        'start': 0,
        'l': ''
    }