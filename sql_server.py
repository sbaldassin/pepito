import json
import logging

from flask import Flask
from flask import request

from tests.config.config import get_config
from tests.db.repositories.q_net_customer_repository import QNetCustomerRepository
from tests.db.repositories.q_net_dw_dim_game_lottery_repository import QNetDwDimGameLotteryRepository
from tests.db.repositories.q_net_dw_dim_game_parimutuel_repository import QNetDwDimGameParimutuelRepository
from tests.db.repositories.q_net_dw_dim_game_sports_repository import QNetDwDimGameSportsRepository
from tests.db.repositories.q_net_dw_fact_bonus_repository import QNetDwFactBonusRepository
from tests.db.repositories.q_net_dw_fact_signin_repository import QNetDwFactSignInRepository
from tests.db.repositories.q_net_dw_fact_signup_repository import QNetDwFactSignupRepository
from tests.db.repositories.q_net_fact_revenue_repository import QNetDWFactRevenueRepository
from tests.db.repositories.q_net_dw_fact_wager_repository import QNetDwFactWagerRepository
from tests.db.repositories.q_net_fact_withdrawal_repository import QNetDWFactWithdrawalRepository
from tests.db.repositories.q_net_task_apx_repository import QNetTaskApxRepository


logging.basicConfig(level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def hello():
    return "Test framework server to get data from the DB"


@app.route('/customer/first')
def get_first_customer():
    customer = QNetCustomerRepository().get_first()
    logging.info("Customer: {}".format(customer))
    return json.dumps(customer, default=str)


@app.route('/customer')
def get_customer_by_id():
    customer_id = request.args.get("customer_id")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    customers = QNetCustomerRepository().get_by_external_customer_id_and_merchant_id(customer_id, merchant_id)
    logging.info("Customers: {}".format(customers))
    return json.dumps(customers, default=str)


@app.route('/customer_by_name_and_merchant')
def get_customer_by_name_and_merchant_id():
    name = request.args.get("name")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    customers = QNetCustomerRepository().get_by_name_and_merchant_id(name, merchant_id)
    logging.info("Customer: {}".format(customers))
    return json.dumps(customers, default=str)


@app.route('/sign_up')
def get_sign_up_by_customer_id():
    customer_id = request.args.get("customer_id")
    sign_up = QNetDwFactSignupRepository().get_by_external_customer_id(customer_id)
    logging.info("Customers: {}".format(sign_up))
    return json.dumps(sign_up, default=str)


@app.route('/sign_in')
def get_sign_in_by_customer_id():
    customer_id = request.args.get("customer_id")
    sign_up = QNetDwFactSignInRepository().get_by_external_customer_id(customer_id)
    logging.info("Customers: {}".format(sign_up))
    return json.dumps(sign_up, default=str)


@app.route('/withdrawals')
def get_withdrawals_by_customer_id():
    customer_id = request.args.get("customer_id")
    withdrawals = QNetDWFactWithdrawalRepository().get_by_external_customer_id(customer_id)
    logging.info("Withdrawals: {}".format(withdrawals))
    return json.dumps(withdrawals, default=str)


@app.route('/deposits')
def get_deposits_by_customer_id():
    customer_id = request.args.get("customer_id")
    deposits = QNetDWFactRevenueRepository().get_by_external_customer_id(customer_id)
    logging.info("Deposits: {}".format(deposits))
    return json.dumps(deposits, default=str)


@app.route('/bonuses')
def get_bonuses_by_customer_id():
    customer_id = request.args.get("customer_id")
    bonuses = QNetDwFactBonusRepository().get_by_external_customer_id(customer_id)
    logging.info("Deposits: {}".format(bonuses))
    return json.dumps(bonuses, default=str)


@app.route('/wagers')
def get_wagers_by_customer_id():
    customer_id = request.args.get("customer_id")
    wagers = QNetDwFactWagerRepository().get_by_external_customer_id(customer_id)
    logging.info("Deposits: {}".format(wagers))
    return json.dumps(wagers, default=str)


@app.route('/wagers/parimutuel')
def get_wagers_parimutuel_by_customer_id():
    customer_id = request.args.get("customer_id")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    wagercount = request.args.get("wagercount")
    if wagercount:
        wagers = QNetDwFactWagerRepository().get_by_external_customer_id_and_wagercount(customer_id, wagercount, merchant_id)
    else:
        wagers = QNetDwFactWagerRepository().get_by_external_customer_id_and_merchant_id(customer_id, merchant_id)
    logging.info("Wagers: {}".format(wagers))
    return json.dumps(wagers, default=str)


@app.route('/games/parimutuel')
def get_game_parimutuel_by_customer_id():
    event_id = request.args.get("event_id")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    breed = request.args.get("breed")
    if not breed:
        games = QNetDwDimGameParimutuelRepository().get_by_event_id(event_id, merchant_id)
    else:
        games = QNetDwDimGameParimutuelRepository().get_by_breed(breed, merchant_id)
    logging.info("Game parimutuel: {}".format(games))
    return json.dumps(games, default=str)


@app.route('/games/lottery')
def get_game_lottery():
    name = request.args.get("name")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    category = request.args.get("category")
    games = QNetDwDimGameLotteryRepository().get_by_name_category(name, category, merchant_id)

    logging.info("Game parimutuel: {}".format(games))
    return json.dumps(games, default=str)


@app.route('/games/sports')
def get_game_sports():
    event_id = request.args.get("event_id")
    merchant_id = request.args.get("merchant_id", int(get_config().get("api", "merchant_id")))
    event = request.args.get("event")
    if not event:
        games = QNetDwDimGameSportsRepository().get_by_event_id(event_id, merchant_id)
    else:
        games = QNetDwDimGameSportsRepository().get_by_event(event, merchant_id)

    logging.info("Game parimutuel: {}".format(games))
    return json.dumps(games, default=str)


@app.route('/tasks')
def get_task_by_task_id():
    task_id = request.args.get("task_id")
    games = QNetTaskApxRepository().get_by_task_id(task_id)
    logging.info("Task: {}".format(games))
    return json.dumps(games, default=str)


if __name__ == '__main__':
    app.run(host='0.0.0.0')