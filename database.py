from pymongo import MongoClient
import time
import uuid
import json

client = MongoClient("localhost", 5555)
# db = client.GUID_DB
db = client["GUID_DB"]
THIRTY_DAYS_IN_SECONDS = 2592000


def getUnixTime():
    unixTime = int(time.time())
    return unixTime

def getExpiration():
    return getUnixTime() + THIRTY_DAYS_IN_SECONDS

def createGUID():

    #Create value
    GUID = uuid.uuid1()
    print(GUID)
    
    #Check that it doesn't exist in dictionary

    #If it does, make a new GUID

    #return GUID
    return GUID


# def checkDatabaseExists():
#     #Check if DB exists
#     databases = client.database_names()
#     if "GUID_DB" in databases:
#         print("EXISTS")
#     else:
#         #if DB doesn't exist, create it
#         db = client.GUID_DB

def createEntry():
    GUID = {
        "guid": createGUID(),
        "expire": getExpiration(),
        "user": "Cylance, Inc."
    }
    print("here")
    print(db)
    print(db.get_collection)

    # data = db.create_collection("GUID")
    data = db["guid"]
    print("collection created")
    col = data[GUID]
    print(data[col])

    print("data input")


def main():
    createEntry()

if __name__ == "__main__":
    main()