from .base_setting import BaseSetting

class LinkedInSetting(BaseSetting):
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