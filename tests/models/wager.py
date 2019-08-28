

class Casino:

    def __init__(self, game_type, game_identifier, currency, value, transaction_date, count):
        self.GameType = game_type
        self.GameIdentifier = game_identifier
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerCasinoFact:

    def __init__(self, player, wager):
        self.player_id = player.PlayerID
        self.currency = wager.Currency
        self.amount = wager.Value
        self.name = wager.GameIdentifier
        self.cateory = wager.GameType
        self.date = wager.TransactionDate
        self.count = wager.Count
        self.channel = 1

    def to_csv(self):
        return [self.player_id, self.currency, self.amount, self.name, self.cateory, self.date, self.count, self.channel]

    def to_csv_with_mappings(self):
        return [self.currency, self.amount, self.name, self.cateory, self.date, self.count, self.channel, self.player_id]

    @staticmethod
    def get_headers():
        return ["currency", "amount", "name", "cateory", "date", "count", "channel", "player_id"]

class Sport:

    def __init__(self, sport, league, event, live, event_id, currency, value, transaction_date, count):
        self.Sport = sport
        self.League = league
        self.Event = event
        self.Live = live
        self.EventID = event_id
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerSportFact:

    def __init__(self, player, sport):
        self.player_id = player.PlayerID
        self.currency = sport.Currency
        self.amount = sport.Value
        self.sport = sport.Sport
        self.league = sport.League
        self.event = sport.Event
        self.live = sport.Live
        self.event_date = sport.TransactionDate
        self.wager_date = sport.TransactionDate
        self.count = sport.Count
        self.channel = 1

    def to_csv(self):
        return [self.player_id, self.currency, self.amount, self.sport, self.league,
                self.event, self.live, self.event_date, self.wager_date, self.count, self.channel]

    def to_csv_with_mappings(self):
        return [self.currency, self.amount, self.sport, self.league, self.event, self.live,
                self.event_date, self.wager_date, self.count, self.channel, self.player_id]

    @staticmethod
    def get_headers():
        return ["currency", "amount", "sport", "league", "event", "live", "event_date", "wager_date", "count", "channel", "player_id"]


class Bet:

    def __init__(self, event_category, event_date, event, currency, value, transaction_date, count):
        self.EventCategory = event_category
        self.Event = event
        self.EventDate = event_date
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class Esport:

    def __init__(self, game, league, event_id, event_category, event_date, event,
                 currency, value, transaction_date, count):
        self.Game = game
        self.League = league
        self.EventID = event_id
        self.EventCategory = event_category
        self.Event = event
        self.EventDate = event_date
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class Lottery:

    def __init__(self, name, category, draw_date, currency, value, transaction_date, count):
        self.Name = name
        self.Category = category
        self.DrawDate = draw_date
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerLotteryFact:

    def __init__(self, player, wager):
        self.player_id = player.PlayerID
        self.currency = wager.Currency
        self.amount = wager.Value
        self.name = wager.Name
        self.category = wager.Category
        self.draw_date = wager.DrawDate
        self.transaction_date = wager.TransactionDate
        self.count = wager.Count
        self.channel = 1

    @staticmethod
    def get_headers():
        return ["currency", "amount", "name", "category", "draw_date", "transaction_date", "count", "channel", "player_id"]

    def to_csv_with_mappings(self):
        return [self.currency, self.amount, self.name, self.category, self.draw_date,
                self.transaction_date, self.count, self.channel, self.player_id]

    def to_csv(self):
        return [self.player_id, self.currency, self.amount, self.name, self.category,
                self.draw_date, self.transaction_date, self.count, self.channel]


class Parimutuel:

    def __init__(self, currency, value, transaction_date, count):
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerParimutuelFact:

    def __init__(self, player, wager):
        self.player_id = player.PlayerID
