import time
import uuid

THIRTY_DAYS_IN_SECONDS = 2592000
def getUnixTime():
    unixTime = int(time.time())
    return unixTime

def getExpiration():
    return getUnixTime() + THIRTY_DAYS_IN_SECONDS

def createGUID():
    #Create value
    GUID = uuid.uuid4()

    print(GUID)

    return GUID