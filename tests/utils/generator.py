import datetime
import random
import string


def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def generate_random_int(length=5):
    return ''.join(random.choice(string.digits) for _ in range(length))


def generate_random_country_code():
    valid_country_codes = ["US", "ES", "AR", "BR", "CA", "UK"]
    return random.choice(valid_country_codes)


def generate_random_language_code():
    languages = ["es", "it", "en"]
    return random.choice(languages)


def generate_random_phone_number():
    return "{}-{}-{}".format(
        generate_random_int(2), generate_random_int(4), generate_random_int(5))


def generate_random_date(years=None, include_time=None, is_future=False):
    if not years:
        years = random.choice(range(5))
    
    date_format = '%Y-%m-%d'
    if include_time:
        date_format = '%Y-%m-%d %H:%M:%S'

    if is_future:
        dt = datetime.datetime.now() + datetime.timedelta(days=years * 365)
    else:
        dt = datetime.datetime.now() - datetime.timedelta(days=years * 365)

    return dt.strftime(date_format)


def generate_random_state():
    valid_states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE"]
    return random.choice(valid_states)


def generate_random_boolean():
    return random.choice([True, False])


def generate_random_currency():
    return random.choice(['USD', 'EUR'])


def generate_random_productid():
    return random.choice(['0', '1', '2', '3', '4', '5', '6'])
