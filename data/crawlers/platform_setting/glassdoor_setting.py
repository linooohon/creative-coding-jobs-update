from .base_setting import BaseSetting

class GlassDoorSetting(BaseSetting):
    # https://www.glassdoor.com/Job/jobs.htm?sc.keyword=creative%20developer
    platform_name = 'glassdoor'
    platform_url = 'https://www.glassdoor.com/Job/jobs.htm?'
    query = {
        'sc.keyword': 'sound design',
        'fromAge': 14,
    }
    referer_list = [
        'https://www.glassdoor.com/',
    ]