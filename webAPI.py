import tornado
import asyncio
import database
import utils
import cache
import json

DEFAULT_USER = "Cylance, Inc."
CACHE_SIZE = 5
DEBUG = True

class GUIDHandler(tornado.web.RequestHandler):
    #READ
    def get(self, guid):
        #Get data from cache
        entry = cache.getGUID(guid)
        #If data is not in cache, get from database
        if entry == None:
            print("Not in cache, going to database")
            entry = database.getEntry(guid)
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
        
        cache.storeGUID(guid, {"guid": guid, "expire": expiration, "user": user}, 100000)
        database.createEntry(guid, expiration, user)

        #Write the dict to the endpoint
        self.write(database.getEntry(guid))
        
        if DEBUG:
            print(f"STORED: {guid}")

    #DELETE
    #delete info from database. Provide no output
    def delete(self, guid):
        cache.deleteGUID(guid)
        database.deleteEntry(guid)
        if DEBUG:
            print(f"DELETED: {guid}")

def make_app():
    return tornado.web.Application([(r"/guid/(.*)", GUIDHandler)])

async def main():
    app = make_app()
    app.listen(5555)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())