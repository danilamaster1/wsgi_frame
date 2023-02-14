from views import Index, Catalog, Contacts
from datetime import date


def date_front(request: dict):
    request['date'] = date.today()


fronts = [date_front]

routes = {
    '/': Index(),
    '/catalog/': Catalog(),
    '/contacts/': Contacts(),
}

