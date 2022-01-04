from .base_setting import BaseSetting

class IndeedUKSetting(BaseSetting):
    # https://jp.indeed.com/jobs?q=frontend%20engineer&l=
    platform_name = 'indeed_uk'
    platform_url = 'https://uk.indeed.com/jobs?'
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

