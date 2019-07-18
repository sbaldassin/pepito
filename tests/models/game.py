from tests.utils.generator import generate_random_date


class CasinoGame:

    def __init__(self, game_type="Video slot", game_identifier="Dracula 2"):
        self.GameType = game_type
        self.GameIdentifier = game_identifier

    def to_csv(self):
        return [self.GameType, self.GameIdentifier]


class BetGame:

    def __init__(self,
                 event="Rainy day",
                 event_category="Weather",
                 event_date=generate_random_date(is_future=True)):
        self.Event = event
        self.EventCategory = event_category
        self.EventDate = event_date


class SportGame:

    def __init__(self,
                 sport="Football",
                 league="Serie A",
                 event="AC Milan vs Juventus FC",
                 live=True,
                 event_date=generate_random_date(is_future=True)):
        self.Sport = sport
        self.League = league
        self.Event = event
        self.Live = live
        self.EventDate = event_date


class EsportGame:

    def __init__(self,
                 game="CS Zero",
                 league="League 1",
                 event="Mark Brown vs Matt White",
                 event_category="Day 2",
                 event_date=generate_random_date(is_future=True)):
        self.Game = game
        self.League = league
        self.Event = event
        self.EventCategory = event_category
        self.EventDate = event_date


class LotteryGame:

    def __init__(self, name="Euro Millions", category="EU Based Lottery", draw_date=generate_random_date()):
        self.Name = name
        self.Category = category
        self.DrawDate = draw_date


class ParimutuelGame:

    def __init__(self, event="Horse race 2019", breed="Harness Power 1000",
                 event_date=generate_random_date(is_future=True)):
        self.Event=event
        self.Breed = breed
        self.EventDate = event_date
