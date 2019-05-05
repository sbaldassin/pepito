

class Wager:

    def __init__(self, game_type, game_identifier, currency, value, transaction_date, count):
        self.GameType = game_type
        self.GameIdentifier = game_identifier
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class ParimutuelWager:

    def __init__(self, currency, value, transaction_date, count):
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count
