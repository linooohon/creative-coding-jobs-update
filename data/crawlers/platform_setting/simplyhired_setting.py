from .base_setting import BaseSetting

class SimplyHiredSetting(BaseSetting):
    platform_name = 'simplyhired'
    platform_url = 'https://www.simplyhired.com/search?'
    query = {
        'q': 'sound design',
        'pn': '1',
    }
    referer_list = [
        'https://www.simplyhired.com/',
    ]