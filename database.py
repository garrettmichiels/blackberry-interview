from pymongo import MongoClient

client = MongoClient("localhost", 5555)
db = client["GUID_DB"]
collection = db["GUIDs"]

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

#Return {} if no match
def getEntry(guid):
    cursor = collection.find({'guid': guid})
    entry = list(cursor)
    #Should only have 1 entry per curser due to the update function
    #If no entry matching
    if len(entry) == 0:
        return None
    guidEntry = entry[0]

    data = {"guid": guidEntry["guid"], "expire": guidEntry["expire"], "user": guidEntry["user"]}
    return data

def deleteEntry(guid):
    collection.delete_one({'guid': guid})

# def main():
#     pass

# if __name__ == "__main__":
#     main()