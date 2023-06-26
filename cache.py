import redis
print("cache")
cache = redis.Redis(host='localhost', port=6379, decode_responses=True)

def storeGUID(guid, metadata, timeToExp):

    cache.hset(guid, mapping=metadata)
    cache.expire(guid, timeToExp)

def getGUID(guid):
    if cache.exists(guid):
        return cache.hgetall(guid)
    return None

#delete in cache
def deleteGUID(guid):
    cache.delete(guid)


