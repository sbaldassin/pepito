

class Withdrawal:

    def __init__(self, amount, currency, transaction_date):
        self.amount = amount
        self.currency = currency
        self.TransactionDate = transaction_date


class WithdrawalFact:

    def __init__(self, player, withdrawal):
        self.player_id = player.PlayerID
        self.currency = withdrawal.currency
        self.amount = withdrawal.amount
        self.transaction_date = withdrawal.TransactionDate

    def to_csv(self):
        return [self.player_id, self.currency, self.amount, self.transaction_date]
