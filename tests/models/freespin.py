

class Freespin:

    def __init__(self, identifier, value, transaction_date):
        self.Identifier = identifier
        self.Value = value
        self.TransactionDate = transaction_date

    def to_csv(self):
        return [self.Identifier, self.Value]
