from quopri import decodestring
from requests import GetRequests, PostRequests


class Page404:
    def __call__(self, requests):
        return '404 bad_request', '404 PAGE NOT FOUND'


class Framework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = Page404()

        requests = {}

        method = environ['REQUEST_METHOD']
        requests['method'] = method
        if method == 'GET':
            request_params = GetRequests().get_params(environ)
            requests['request_params'] = self.decode_get_params(request_params)
            print(f"params -> {requests['request_params']}")
        if method == 'POST':
            data = PostRequests().get_params(environ)
            requests['data'] = self.decode_post_data(data)
            print(f'data -> {requests["data"]}')

        for front in self.fronts:
            front(requests)

        code, body = view(requests)
        start_response(code, [('Content_Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_get_params(data):
        new_data = {}
        for k, v in data.items():
            key = bytes(k.replace('%', '=').replace("+", ' '), 'UTF-8')
            key_decode_str = decodestring(key).decode('UTF-8')

            val = bytes(v.replace('%', '=').replace("+", ' '), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[key_decode_str] = val_decode_str
        return new_data

    @staticmethod
    def decode_post_data(data):
        new_data = {}
        for k, v in data.items():
            val = bytes(v.replace('%', '=').replace("+", ' '), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            new_data[k] = val_decode_str
        return new_data
