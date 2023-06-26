import redis

# A class that modifies a Redis cache by connecting to a Redis server on the given host and port.
class Cache():
    def __init__(self, host, port):
        self.cache = redis.Redis(host=host, port=port, decode_responses=True)

    #Create a hash entry with the guid and its other metadata (includes the guid itself)
    #The stored guid only lasts until the _timeToExp_
    def storeGUID(self, guid, metadata, timeToExp):
        self.cache.hset(guid, mapping=metadata)
        self.cache.expireat(guid, timeToExp)

    #Get the guid if it is in the cache, otherwise, return None
    def getGUID(self, guid):
        if self.cache.exists(guid):
            return self.cache.hgetall(guid)
        return None

    #Delete an entry in the cache
    def deleteGUID(self, guid):
        self.cache.delete(guid)


