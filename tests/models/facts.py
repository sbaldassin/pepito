

class BonusFact:

    def __init__(self, player, bonus):
        self.player_id = player.PlayerID
        self.description = bonus.Identifier
        self.product_id = bonus.ProductID
        self.currency = bonus.Currency
        self.value = bonus.Value
        self.activity_time = bonus.TransactionDate

    def to_csv(self):
        return [self.player_id, self.description, self.product_id, self.currency, self.value, self.activity_time]


class FreeSpinFact:

    def __init__(self, player, free_spin):
        self.player_id = player.PlayerID
        self.description = free_spin.Identifier
        self.number_of_free_spin = free_spin.Value
        self.activity_date = free_spin.TransactionDate

    def to_csv(self):
        return [self.player_id, self.description, self.number_of_free_spin, self.activity_date]
