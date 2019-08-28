

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

    def to_csv_with_mappings(self):
        return [self.description, self.product_id, self.currency, self.value, self.activity_time, self.player_id]

    @staticmethod
    def get_headers():
        return ["description", "product_id", "currency", "value", "activity_time", "player_id"]


class FreeSpinFact:

    def __init__(self, player, free_spin):
        self.player_id = player.PlayerID
        self.description = free_spin.Identifier
        self.number_of_free_spin = free_spin.Value
        self.activity_date = free_spin.TransactionDate

    def to_csv_with_mappings(self):
        return [self.description, self.number_of_free_spin, self.activity_date, self.player_id]

    def to_csv(self):
        return [self.player_id, self.description, self.number_of_free_spin, self.activity_date]

    @staticmethod
    def get_headers():
        return ["description", "free_spin_number", "activity_time", "player_id"]
