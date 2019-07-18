

class Bonus:

    def __init__(self, product_id, identifier, currency, value, transaction_date):
        self.ProductID = product_id
        self.Identifier = identifier
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date

    def to_csv(self):
        return [self.Identifier, self.ProductID]
