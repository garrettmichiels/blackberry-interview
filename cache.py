import redis

# A class that modifies a Redis cache by connecting to a Redis server on the given host and port.
class Cache():
    def __init__(self, host, port, maxKeys):
        self.cache = redis.Redis(host=host, port=port, decode_responses=True)
        self.maxKeys = maxKeys
        

    # Create a hash entry with the guid and its other metadata (includes the guid itself)
    # The cache only stores _maxKeys_ amount of keys
    def storeGUID(self, guid, expiration, user):
        metadata = {"guid": guid, "expire": expiration, "user": user}
        #Remove the nearest expiration if maxKeys reached
        if self.cache.dbsize() >= self.maxKeys:
            sortedListOfKeys = sorted(self.cache.keys("*"), key=lambda x: self.cache.hgetall(x)["expire"])
            self.deleteGUID(sortedListOfKeys[0])
        self.cache.hset(guid, mapping=metadata)

    # Get the guid if it is in the cache, otherwise, return None
    # The cache only has one instance of each GUID since POST will only update if it exists already
    def getGUID(self, guid):
        if self.cache.exists(guid):
            return self.cache.hgetall(guid)
        return None

    # Delete an entry in the cache
    def deleteGUID(self, guid):
        self.cache.delete(guid)
