from pymongo import MongoClient
import mysql.connector
import time
import json


client = MongoClient("localhost", 5555)
db = client["GUID_DB"]
collection = db["GUIDs"]


# def checkDatabaseExists():
#     #Check if DB exists
#     databases = client.database_names()
#     if "GUID_DB" in databases:
#         print("EXISTS")
#     else:
#         #if DB doesn't exist, create it
#         db = client.GUID_DB

#TODO: maybe pass in guid, expiration, and name
def createEntry(guid, expiration, user):
    GUID = {
        "guid": guid,
        "expire": expiration,
        "user": user
    }
    #Check if guid exists, if so, only update the expiration
    if collection.count_documents({'guid': guid}) > 0:
        print("Update")
        collection.update_one({'guid': guid}, {"$set":{'expire': expiration}})
    #if guid doesn't exist, insert
    else:
        collection.insert_one(GUID)
    # data.insert_one(guid)
    # col = collection[guid]


def getEntry(guid):
    x = collection.find({'guid': guid})
    #Should only have 1 entry per curser due to the update function
    for curser in x:
        data = {"guid": curser["guid"], "expire": curser["expire"], "user": curser["user"]}
    return data

def deleteEntry(guid):
    collection.delete_one({'guid': guid})

def main():
    createEntry()

if __name__ == "__main__":
    main()