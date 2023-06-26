from pymongo import MongoClient
import time

# A class that accesses a MongoDB Server on the given host and port to modify a database. 
# A new database will only be created if it doesn't exist
class Database():
    def __init__(self, host, port):
        self.client = MongoClient(host, port)
        self.db = self.client["GUID_DB"]
        self.collection = self.db["GUIDs"]

    def createEntry(self, guid, expiration, user):
        GUID = {
            "guid": guid,
            "expire": expiration,
            "user": user
        }
        #Check if guid exists, if so, only update the expiration
        if self.collection.count_documents({'guid': guid}) > 0:
            self.collection.update_one({'guid': guid}, {"$set":{'expire': expiration}})
        #if guid doesn't exist, insert
        else:
            self.collection.insert_one(GUID)

    #Return None if no match
    def getEntry(self, guid):
        cursor = self.collection.find({'guid': guid})
        entry = list(cursor)
        #Should only have 1 entry per curser due to the update function
        #If no entry matching
        if len(entry) == 0:
            return None
        guidEntry = entry[0]
        data = {"guid": guidEntry["guid"], "expire": guidEntry["expire"], "user": guidEntry["user"]}
        return data

    #Deletes an entry in a the collection with the corresponding guid
    def deleteEntry(self, guid):
        self.collection.delete_one({'guid': guid})
      
    #Deletes guid's with expire fields before the current Unix time
    def findExpiredEntries(self):
        expiredGUIDs = []
        currentTime = time.time()
        cursor = self.collection.find()
        for entry in cursor:
            if int(entry["expire"]) < currentTime:
                expiredGUIDs.append(entry["guid"])
        return expiredGUIDs
            