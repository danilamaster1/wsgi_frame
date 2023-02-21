from wsgiref.simple_server import make_server

from danni_framework.main import Framework
from urls import fronts
from views import routes

frame = Framework(routes, fronts)

with make_server('', 8000, frame) as httpd:
    print("Server on port 8000...")
    httpd.serve_forever()
