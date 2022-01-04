from .base_setting import BaseSetting

class IndeedJPSetting(BaseSetting):
    # https://jp.indeed.com/jobs?q=frontend%20engineer&l=
    platform_name = 'indeed_jp'
    platform_url = 'https://jp.indeed.com/jobs?'
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
