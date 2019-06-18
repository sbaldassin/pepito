import logging
from time import sleep

import requests


def get_until_not_empty(url, timeout=100):
    count = 0
    result = []
    while count < timeout and result == []:
        result = requests.get(url).json()
        logging.info("API response: {}".format(result))

        if result == []:
            logging.info("Result is empty. Sleeping for 10 secs")
            sleep(10)
            count += 10
    return result


def get_until_attempt_greater_than_zero(url, timeout=100):
    count = 0
    result = []
    while count < timeout:
        result = requests.get(url).json()
        logging.info("API response: {}".format(result))

        if result:
            if result[0]["Attempts"] > 0:
                break

        logging.info("Result is empty or attempt is 0. Sleeping for 10 secs")
        sleep(10)
        count += 10

    return result