import json
import logging
from flask import Flask
from flask import request

from tests.db.repositories.q_net_customer_repository import QNetCustomerRepository
from tests.db.repositories.q_net_dw_fact_signup_repository import QNetDwFactSignupRepository
from tests.db.repositories.q_net_fact_withdrawal_repository import QNetDWFactWithdrawalRepository

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
    customers = QNetCustomerRepository().get_by_external_customer_id(customer_id)
    logging.info("Customers: {}".format(customers))
    return json.dumps(customers, default=str)


@app.route('/customer_by_name_and_merchant')
def get_customer_by_name_and_merchant_id():
    name = request.args.get("name")
    merchant_id = request.args.get("merchant_id")
    customers = QNetCustomerRepository().get_by_name_and_merchant_id(name, merchant_id)
    logging.info("Customer: {}".format(customers))
    return json.dumps(customers, default=str)


@app.route('/sign_up')
def get_sign_up_by_customer_id():
    customer_id = request.args.get("customer_id")
    sign_up = QNetDwFactSignupRepository().get_by_external_customer_id(customer_id)
    logging.info("Customers: {}".format(sign_up))
    return json.dumps(sign_up, default=str)


@app.route('/withdrawals')
def get_withdrawals_by_customer_id():
    customer_id = request.args.get("customer_id")
    withdrawals = QNetDWFactWithdrawalRepository().get_by_external_customer_id(customer_id)
    logging.info("Withdrawals: {}".format(withdrawals))
    return json.dumps(withdrawals, default=str)


if __name__ == '__main__':
    app.run(host='0.0.0.0')