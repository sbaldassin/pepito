

class Revenue:

    def __init__(self, amount, currency, transaction_date, success, payment_method):
        self.Amount = amount
        self.Currency = currency
        self.TransactionDate = transaction_date
        self.PaymentMethod = payment_method
        self.Sucess = success