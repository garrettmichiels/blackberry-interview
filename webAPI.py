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
        entry = None #cache.getGUID(guid)
        print(entry)
        #If data is not in cache, get from database
        if entry == None:
            entry = database.getEntry(guid)

        self.write(f"{entry}")
        
    #CREATE/UPDATE
    #If the guid already exists, overwrite by providing the same guid, perfect. Otherwise, make a separate funciotnality for update
    def post(self, guid=None):
        if guid == None:
            guid = utils.createGUID()

        body = json.loads(self.request.body)
        user = body["user"]
        expiration = body["expire"]
        if body["expire"] == None:
            expiration = utils.getExpiration()

        if body["user"] == None:
            user = DEFAULT_USER
        
        cache.storeGUID(guid, {"guid": guid, "expire": expiration, "user": user}, 100000)
        database.createEntry(guid, expiration, user)
        
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
    return tornado.web.Application([
        (r"/guid/(.*)", GUIDHandler),
    ])

async def main():
    app = make_app()
    app.listen(5555)
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())