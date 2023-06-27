import tornado
import asyncio
from database import Database
from cache import Cache
import utils
import json
import argparse

DEFAULT_USER = "Cylance, Inc."
DEFAULT_HOST = "localhost"
DEFAULT_API_PORT = 8888
DEFAULT_DB_PORT = 5555
DEFAULT_CACHE_PORT = 6379
MAX_CACHE_KEYS = 3

class GUIDHandler(tornado.web.RequestHandler):
    #Initialize is run upon each request
    def initialize(self):
        #Checks for expired GUIDs and then deletes them
        expiredGUIDs = database.findExpiredEntries()
        for guid in expiredGUIDs:
            debugMessage(f"Expired GUID removed from cache and database: {guid}")
            database.deleteEntry(guid)
            cache.deleteGUID(guid)

    #READ method: Get the GUID from the cache or database
    #None is returned when a GUID can't be found in the cache or database
    def get(self, guid):
        try:
            entry = cache.getGUID(guid)
        except:
            self.writeMsgAndStatus("Cannot connect to Redis Server", 500)
            return
        #If data is not in cache, get from database
        if entry == None:
            debugMessage("Not in cache. Searching database...")
            try:
                entry = database.getEntry(guid)
            except:
                self.writeMsgAndStatus("Cannot connect to MongoDB Server", 500)
                return
            #If not in database, send message and 500 status
            if entry == None:
                self.writeMsgAndStatus("That GUID doesn't exist", 500)
                return
        self.writeMsgAndStatus(entry, 200)

    #CREATE/UPDATE method: Create or update the given GUID
    #If the GUID exists, storeGUID and createEntry will simply update the expiration
    def post(self, guid=utils.createGUID()):
        try:
            body = json.loads(self.request.body)
        except:
            #If given json cannot be read, send client error
            self.writeMsgAndStatus("The JSON body provided was invalid for this API", 400)
            return
        
        #Set variables to provided values. If not provided, set to defaults.
        user = body.get("user", DEFAULT_USER)
        expiration = body.get("expire", utils.getExpiration())

        #Store in cache and database
        cache.storeGUID(guid, expiration, user)
        database.createEntry(guid, expiration, user)

        #Write the dict to the endpoint
        self.writeMsgAndStatus(database.getEntry(guid), 201)
        debugMessage(f"STORED: {guid}")

    #DELETE method: Delete info from database. Provide no output
    def delete(self, guid):
        cache.deleteGUID(guid)
        database.deleteEntry(guid)
        debugMessage(f"DELETED: {guid}")

    def writeMsgAndStatus(self, message, status):
        self.set_status(status)
        self.write(message)

def debugMessage(message):
    if DEBUG:
        print(message)

async def main():
    app = tornado.web.Application([(r"/guid/(.*)", GUIDHandler),])
    app.listen(args.apiPort)
    print("API listening...")
    await asyncio.Event().wait()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--apiPort", type=int, default=DEFAULT_API_PORT)
    parser.add_argument("--dbHost", type=str, default=DEFAULT_HOST)
    parser.add_argument("--dbPort", type=int, default=DEFAULT_DB_PORT)
    parser.add_argument("--cacheHost", type=str, default=DEFAULT_HOST)
    parser.add_argument("--cachePort", type=int, default=DEFAULT_CACHE_PORT)
    parser.add_argument("--debug", type=bool, default=False)
    args = parser.parse_args()

    #Start connection to database and cache
    database = Database(args.dbHost, args.dbPort)
    cache = Cache(args.cacheHost, args.cachePort, MAX_CACHE_KEYS)

    DEBUG = args.debug
    asyncio.run(main())