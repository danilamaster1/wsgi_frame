class GetRequests:
    @staticmethod
    def parse_params(data: str):
        result = {}
        if data:
            params = data.split('&')
            for i in params:
                k, v = i.split('=')
                result[k] = v
        return result

    def get_params(self, environ):
        query_string = environ['QUERY_STRING']
        params = self.parse_params(query_string)
        return params


class PostRequests:
    @staticmethod
    def parse_params(data: str):
        result = {}
        if data:
            params = data.split('&')
            for i in params:
                k, v = i.split('=')
                result[k] = v
        return result

    @staticmethod
    def get_wsgi_input_data(env):
        content_len_data = env.get('CONTENT_LENGTH')
        content_len = int(content_len_data) if content_len_data else 0
        data = env['wsgi.input'].read(content_len) if content_len > 0 else b''
        return data

    def parse_wsgi_input_data(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.parse_params(data_str)
        return result

    def get_params(self, environ):
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)
        return data
