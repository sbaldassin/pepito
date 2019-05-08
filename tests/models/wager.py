

class WagerCasino:

    def __init__(self, game_type, game_identifier, currency, value, transaction_date, count):
        self.GameType = game_type
        self.GameIdentifier = game_identifier
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerSport:

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


class WagerBet:

    def __init__(self, event_category, event_date, event, currency, value, transaction_date, count):
        self.EventCategory = event_category
        self.Event = event
        self.EventDate = event_date
        self.Currency = currency
        self.Value = value
        self.TransactionDate = transaction_date
        self.Count = count


class WagerEsport:

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


class WagerLottery:

    def __init__(self, name, category, draw_date, currency, value, transaction_date, count):
        self.Name = name
        self.Category = category
        self.DrawDate = draw_date
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
