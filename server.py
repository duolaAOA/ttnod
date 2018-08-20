# -*-coding:utf-8 -*-

from tornado.ioloop import IOLoop
import tornado.web
from tornado.httpserver import HTTPServer
from tornado.options import define, options

from settings import setting
from handler.routes import Route


define("port", default=8008, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, settings):
        route_handlers = Route.get_route()

        super(Application, self).__init__(route_handlers, **settings)


if __name__ == '__main__':
    options.parse_command_line()
    print('Server start to listen ' + str(options.port))
    http_server = HTTPServer(Application(setting))
    http_server.listen(options.port)
    loop = IOLoop.instance()
    loop.start()
