import tornado
import asyncio
from database import Database
from cache import Cache
import utils
import json
import argparse

DEFAULT_USER = "Cylance, Inc."
DEFAULT_DB_PORT = 5555
DEFAULT_CACHE_PORT = 6379
DEFAULT_HOST = "localhost"
CACHE_SIZE = 5
DEBUG = True

class GUIDHandler(tornado.web.RequestHandler):
    def initialize(self, args):
        databaseHost = args["dbHost"]
        databasePort = args["dbPort"]
        cacheHost = args["cacheHost"]
        cachePort = args["cachePort"]

        self.database = Database(databaseHost, databasePort)
        self.cache = Cache(cacheHost, cachePort)

    #READ
    def get(self, guid):
        #Get data from cache
        entry = self.cache.getGUID(guid)
        #If data is not in cache, get from database
        if entry == None:
            print("Not in cache, going to database")
            entry = self.database.getEntry(guid)
            if entry == None:
                return

        self.write(entry)

    #CREATE/UPDATE
    #If the guid already exists, overwrite by providing the same guid, perfect. Otherwise, make a separate funciotnality for update
    def post(self, guid=utils.createGUID()):
        body = json.loads(self.request.body)
        #Set variables to provided values, set to default if none
        if "user" in body:
            user = body["user"]
        else:
            user = DEFAULT_USER
        if "expire" in body:
            expiration = body["expire"]
        else:
            expiration = utils.getExpiration()
        
        self.cache.storeGUID(guid, {"guid": guid, "expire": expiration, "user": user}, 100000)
        self.database.createEntry(guid, expiration, user)

        #Write the dict to the endpoint
        self.write(self.database.getEntry(guid))
        
        if DEBUG:
            print(f"STORED: {guid}")

    #DELETE
    #delete info from database. Provide no output
    def delete(self, guid):
        self.cache.deleteGUID(guid)
        self.database.deleteEntry(guid)
        if DEBUG:
            print(f"DELETED: {guid}")

def make_app():
    return tornado.web.Application([(r"/guid/(.*)", GUIDHandler, dict(args = vars(args))),])

async def main():
    app = make_app()
    app.listen(5555)
    await asyncio.Event().wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dbHost", type=str, default=DEFAULT_HOST)
    parser.add_argument("--dbPort", type=int, default=DEFAULT_DB_PORT)
    parser.add_argument("--cacheHost", type=str, default=DEFAULT_HOST)
    parser.add_argument("--cachePort", type=int, default=DEFAULT_CACHE_PORT)

    args = parser.parse_args()
    print(type(vars(args)))
    print(args)
    asyncio.run(main())