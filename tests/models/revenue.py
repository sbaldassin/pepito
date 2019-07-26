

class Revenue:

    def __init__(self, amount, currency, transaction_date, success, payment_method):
        self.Amount = amount
        self.Currency = currency
        self.TransactionDate = transaction_date
        self.PaymentMethod = payment_method
        self.Sucess = success


class RevenueFact:

    def __init__(self, player, revenue):
        self.player_id = player.PlayerID
        self.currency = revenue.Currency
        self.amount = revenue.Amount
        self.activity_date = revenue.TransactionDate
        self.channel = 1
        self.payment_method = revenue.PaymentMethod
        self.success = revenue.Sucess

    def to_csv(self):
        return [self.player_id, self.currency, self.amount, self.activity_date,
                self.channel, self.payment_method, self.success]
