from .indeed_us import Indeed
from .linkedin_selenium import LinkedIn
from .simplyhired import SimplyHired
from .glassdoor import Glassdoor

from .indeed_jp import IndeedJP
from .indeed_uk import IndeedUK

JOB_BANK_LIST_MONDAY = [Indeed, SimplyHired, IndeedUK, Glassdoor]
# JOB_BANK_LIST = [IndeedJP]
JOB_BANK_LIST_DAILY = [Glassdoor, SimplyHired]

