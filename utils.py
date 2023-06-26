import time
import uuid

#General utility functions

THIRTY_DAYS_IN_SECONDS = 2592000

#Gets the current Unix time
def getUnixTime():
    unixTime = int(time.time())
    return unixTime

#Creates the expire variable's value by using the current unix time and adding thirty days in seconds
def getExpiration():
    return getUnixTime() + THIRTY_DAYS_IN_SECONDS

#Uses the uuid library and removes the dashes
def createGUID():
    #Create value
    GUID = str(uuid.uuid4())
    GUID = GUID.replace("-", "").upper()
    return GUID
