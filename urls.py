from views import Index, Catalog, About
from datetime import date


def date_front(request):
    request['date'] = date.today()


fronts = [date_front]

routes = {
    '/': Index(),
    '/catalog/': Catalog(),
    '/about/': About(),
}

