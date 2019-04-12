import datetime
import random
import string


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_random_int(length=5):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_random_country_code():
    valid_country_codes = ["IT", "EN"]
    return random.choice(valid_country_codes)

def generate_random_language_code():
    languages = ["es","it", "en"]
    return random.choice(languages)

def generate_random_phone_number():
    return "{}-{}-{}".format(
        generate_random_int(2), generate_random_int(4), generate_random_int(5))


def generate_random_date(years=None):
    if not years:
        years = random.choice(range(5))
    dt = datetime.datetime.now() - datetime.timedelta(days=years * 365)
    return dt.strftime('%Y-%m-%d')
