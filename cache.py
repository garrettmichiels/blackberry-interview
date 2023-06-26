import redis
print("cache")

class Cache():
    def __init__(self, host, port):
        self.cache = redis.Redis(host=host, port=port, decode_responses=True)

    def storeGUID(self, guid, metadata, timeToExp):

        self.cache.hset(guid, mapping=metadata)
        self.cache.expire(guid, timeToExp)

    def getGUID(self, guid):
        if self.cache.exists(guid):
            return self.cache.hgetall(guid)
        return None

    #delete in cache
    def deleteGUID(self, guid):
        self.cache.delete(guid)


