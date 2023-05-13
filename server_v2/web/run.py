#!/usr/bin/env
# coding: utf-8
from common import *

class IndexHandler(tornado.web.RequestHandler):
    async def get(self):

        c = MongoMixin.userDb['test']
        # c = db.test_collection
        async for document in c.find({'a': 1}):
            Log.i(document)

        account = MongoMixin.userDb['account']
        account = account.find(
            {
                'contact.0.value': int("917005612276"),
                'privacy.0.value': "trakiga.com"
            },
            {
                '_id': 1
            },
            limit=1
        )
        async for r in account:
            Log.i(r)

        test = MongoMixin.userDb['test']
        updateAccountResult = await test.find_one_and_update(
            {
                'a': 2
            },
            {
                '$set': {
                    'contact': True
                }
            },
            projection={'_id': False}
        )
        # if updateResult['n']:
        Log.i('HH', updateAccountResult)
        Log.i(FN_ENCRYPT('sddd'))

        # for i in rs:
        #    Log.i(i)

        self.finish("It works")


class SleepHandler(tornado.web.RequestHandler):
    async def get(self):
        print("hello tornado")
        # await asyncio.sleep(100)
        for i in range(0, 100000):
            await asyncio.sleep(1)
            Log.i(i)
        self.write('It works!')


class AsyncHttpHandler(tornado.web.RequestHandler):
    async def get(self):
        rs = MongoMixin.userDb.test.find()
        for i in rs:
            Log.i(i)

        url = 'http://127.0.0.1:5000/'
        client = httpclient.AsyncHTTPClient()
        resp = await client.fetch(url)
        print(resp.body)
        self.finish(resp.body)


class GenHttpHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        url = 'http://127.0.0.1:5000/'
        client = httpclient.AsyncHTTPClient()
        resp = yield client.fetch(url)
        print(resp.body)
        self.finish(resp.body)


class SyncHttpHandler(tornado.web.RequestHandler):
    async def get(self):
        url = 'http://127.0.0.1:5000/'
        resp = requests.get(url)
        print(resp.text)
        self.finish(resp.text)


class App(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True
        }
        super(App, self).__init__(
            handlers=[
                (r'/', IndexHandler),
                (r'/async', AsyncHttpHandler),
                (r'/gen', GenHttpHandler),
                (r'/sync', SyncHttpHandler),
                (r'/sleep', SleepHandler),
                (r'/v2/web/api/sign/in', SignInHandler),
                (r'/v2/web/api/sign/up', SignUpHandler),
                #(r'/v2/web/api/pass/qr', PassQRHandler),
                (r'/v2/web/api/booking/Docteradd', DocterListHandler),
                (r'/v2/web/api/booking/clinicadd', ClinicListHandler),
                (r'/v2/web/api/booking/slotadd', SlotListHandler),
                (r'/v2/web/api/booking/cityadd', CityListHandler),
                (r'/v2/web/api/booking/bookingadd', BookingListHandler),
                (r'/v2/web/api/booking/trasactionadd', TransactionListHandler),
                            
            ],
            **settings)
        Log.i('APP', 'Running Tornado Application Port - [ {} ]'.format(WEB_SERVER_PORT))



if __name__ == '__main__':
    # asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # tornado_asyncio.AsyncIOMainLoop().install()
    # app = App()
    # server = httpserver.HTTPServer(app, xheaders=True)
    # server.listen(WEB_SERVER_PORT)
    # asyncio.get_event_loop().run_forever()
    print("Startimmg server")
    app = App()
    app.listen(3333)
    tornado.ioloop.IOLoop.current().start()
