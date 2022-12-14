import random
import string
from datetime import datetime


def datetime_string():
    now = datetime.now()
    return now.strftime('%Y%m%d%H%M%S%f')[:-3]


def random_token(upper=False, k=4):
    param = string.digits

    if upper:
        param = string.ascii_uppercase + string.digits

    return ''.join(random.choices(string.ascii_lowercase + param, k=k))
