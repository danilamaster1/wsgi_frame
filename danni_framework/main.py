class Page404:
    def __call__(self, requests):
        return '404 bad_request', '404 PAGE NOT FOUND'


class Framework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']
        print(path)

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = Page404()
        requests = {}
        for front in self.fronts:
            front(requests)
        code, body = view(requests)
        start_response(code, [('Content_Type', 'text/html')])
        return [body.encode()]
