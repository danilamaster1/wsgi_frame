from danni_framework.templator import render


class Index:
    def __call__(self, requests):
        return '200 OK', render('index.html', date=requests.get('date', None))


class Catalog:
    def __call__(self, requests):
        return '200 OK', render('catalog.html')


class About:
    def __call__(self, requests):
        return '200 OK', render('about.html')
