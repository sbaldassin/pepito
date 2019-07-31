

class Payout:

    def __init__(self, product_id, game, currency, amount, transaction_date, count):
        self.ProductID = product_id
        self.Currency = currency
        self.Amount = amount
        self.TransactionDate = transaction_date
        self.Count = count
        self.Game = game


class PayoutFact:

    def __init__(self, player, payout):
        self.player_id = player.PlayerID
        self.currency = payout.Currency
        self.amount = payout.Amount
        self.product_id = payout.ProductID
        self.activity_time = payout.TransactionDate
        self.payout_count = payout.Count
        self.game = payout.Game

    def to_csv(self):
        csv = [self.player_id, self.currency, self.amount, self.product_id, self.activity_time,
               self.payout_count]

        if self.product_id == 1:
            csv += [self.game["GameIdentifier"], self.game["GameType"]]
        elif self.product_id == 2:
            csv += [self.game["Sport"], self.game["League"], self.game["Event"], self.game["EventDate"], self.game["Live"]]
        elif self.product_id == 3:
            csv += [self.game["Event"], self.game["EventCategory"], self.game["EventDate"]]
        elif self.product_id == 4:
            csv += [self.game["Game"], self.game["League"], self.game["Event"], self.game["EventCategory"], self.game["EventDate"]]
        elif self.product_id == 5:
            csv += [self.game["Name"], self.game["Category"], self.game["DrawDate"]]
        elif self.product_id == 6:
            csv += [self.game["Event"], self.game["Breed"], self.game["EventDate"]]
        return csv
