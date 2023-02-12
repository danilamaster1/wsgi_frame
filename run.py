from wsgiref.simple_server import make_server

from danni_framework.main import Framework
from urls import routes, fronts

frame = Framework(routes, fronts)

with make_server('', 8000, frame) as httpd:
    print("Server on port 8000...")
    httpd.serve_forever()
