

class Event:

    def __init__(self, event, breed, event_date, event_id):
        self.Event = event
        self.Breed = breed
        self.EventDate = event_date
        self.EventID = event_id


class LotteryEvent:

    def __init__(self, name, category, draw_date):
        self.Name = name
        self.Category = category
        self.DrawDate = draw_date
