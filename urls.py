from datetime import date


def date_front(request: dict):
    request['date'] = date.today()


fronts = [date_front]

