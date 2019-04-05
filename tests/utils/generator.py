import datetime
import random
import string


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_random_int(length=5):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_random_country_code():
    return "IT"


def generate_random_phone_number():
    return "{}-{}-{}".format(
        generate_random_int(2), generate_random_int(4), generate_random_int(5))


def generate_random_date(years):
    dt = datetime.datetime.now() - datetime.timedelta(days=years * 365)
    #return "{year}-{month}-{day}".format(year=dt.year, month=dt.month, day=dt.day)
    return "2018-05-18 06:52:27"
