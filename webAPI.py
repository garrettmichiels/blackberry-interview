import tornado
import asyncio
from database import Database
from cache import Cache
import utils
import json
import argparse


DEFAULT_USER = "Cylance, Inc."
DEFAULT_API_PORT = 8888
DEFAULT_DB_PORT = 5555
DEFAULT_CACHE_PORT = 6379
MAX_CACHE_KEYS = 3
DEFAULT_HOST = "localhost"

class GUIDHandler(tornado.web.RequestHandler):
    def initialize(self):
        #Checks for expired GUIDs and then deletes them
        expiredGUIDs = database.findExpiredEntries()
        for guid in expiredGUIDs:
            print("delete")
            database.deleteEntry(guid)
            cache.deleteGUID(guid)

    #READ
    #Get the GUID from the cache or database
    def get(self, guid):
        try:
            entry = cache.getGUID(guid)
        except:
            self.set_status(500)
            self.write("Cannot connect to Redis Server")
            return
        #If data is not in cache, get from database
        if entry == None:
            debugMessage("Not in cache. Searching database...")
            try:
                entry = database.getEntry(guid)
            except:
                self.set_status(500)
                self.write("Cannot connect to MongoDB Server")
                return
            #Not in database
            if entry == None:
                self.set_status(500)
                self.write("That GUID doesn't exist")
                return
        self.set_status(200)
        self.write(entry)

    #CREATE/UPDATE
    #Create or update the given GUID
    #If the GUID exists, storeGUID and createEntry will simply update the expiration
    def post(self, guid=utils.createGUID()):
        try:
            body = json.loads(self.request.body)
        except:
            #If given json cannot be read, send client error
            self.set_status(400)
            self.write("The JSON body provided was invalid for this API")
            return
        #Set variables to provided values, set to default if none
        if "user" in body:
            user = body["user"]
        else:
            user = DEFAULT_USER
        if "expire" in body:
            expiration = body["expire"]
        else:
            expiration = utils.getExpiration()
            debugMessage(f"Created expiration: {expiration}")

        #Store in cahce and database
        cache.storeGUID(guid, {"guid": guid, "expire": expiration, "user": user})
        database.createEntry(guid, expiration, user)

        #Write the dict to the endpoint
        self.set_status(201)
        self.write(database.getEntry(guid))
        
        debugMessage(f"STORED: {guid}")

    #DELETE
    #delete info from database. Provide no output
    def delete(self, guid):
        cache.deleteGUID(guid)
        database.deleteEntry(guid)
        debugMessage(f"DELETED: {guid}")


def make_app():
    return tornado.web.Application([(r"/guid/(.*)", GUIDHandler),])

def debugMessage(message):
    if DEBUG:
        print(message)

async def main():
    app = make_app()
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

    database = Database(args.dbHost, args.dbPort)
    cache = Cache(args.cacheHost, args.cachePort, MAX_CACHE_KEYS)

    DEBUG = args.debug
    asyncio.run(main())