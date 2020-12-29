'''
This is just used as an 'Helper DB' (Neo4j is the main DB) cos I am planning
to run the code on Google Colab and to save data to Neo4j  I have to host it!!
But MongoDB Atlas provides limited hosting (for free 😅).

:: Process - 1 ::
1. Gets the data from main.py
2. Populates the knowledge extracted onto a MongoDB Atlas

:: Process - 2 ::
1. Fetches the data from MongoDB Atlas
2. Populates Neo4j DB with this fetched data
'''

import pymongo 
import sys
import os
os.system("")


class MongoDBC:

    def __init__(self):
        # self.client = MongoClient('mongodb://localhost:27017')
        self.client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.te4lx.mongodb.net/BDA_project?retryWrites=true&w=majority")
        # print(self.client.list_database_names())
        self.db = self.client.BDA_project # select or create this DB
        # print(self.db.list_collection_names())
        self.collection = self.db.FamousPersonality # select the collection
        self.collection.create_index([('doc_name', pymongo.ASCENDING)], unique=True)

    def findOne(self, doc_name: str = None):
        if (doc_name is None):
            return self.collection.find_one()
        else:
            return self.collection.find_one({"doc_name": doc_name})

    def findMany(self, batch_size: int = 5):
        return self.collection.find().limit(batch_size)

    def deleteOne(self, doc_name: str = None):
        if (doc_name != None):
            res = self.collection.find_one_and_delete({"doc_name": doc_name})
            if(res != None):
                print('\033[93m'+"[DELETE] doc_name '{:s}' with _id '{}' is deleted".format(doc_name, res['_id'])+'\033[0m')
            else:
                print('\033[91m'+"[DELETE] doc_name '{:s}' doesn't exists in the MongoDB collection".format(doc_name)+'\033[0m')

    def deleteMany(self, doc_names):
        for doc_name in doc_names:
            self.deleteOne(doc_name)

    def insertOne(self, doc) -> None:
        try:
            returned_id = self.collection.insert_one(doc)
            print("[INSERT] {} is the current inserted doc id".format(returned_id.inserted_id))
        except Exception as e:
            print('\033[93m'+"[INSERT] doc_name '{:s}' already exists in the MongoDB collection".format(doc['doc_name'])+'\033[0m')
            # print('\033[93m'+e+'\033[0m')

    def insertMany(self, list_of_doc) -> None:
        for doc in list_of_doc:
            self.insertOne(doc)
        
    def totalDocCount(self) -> int:
        print("[INFO] Total doc count in the collection is {}".format(self.collection.count_documents({})))


# gets mini_batch from MongoDB Atlas and add them to Neo4j,
# after adding delete the mini_batch from MongoDB Atlas.
def populateNeo4jDB() -> None:
    try:
        mongoDBC_obj = MongoDBC()
        print("[INFO] MongoDB Atlas server is connected")
    except Exception as e:
        print('\033[91m'+"\n[ERR] MongoDB Atlas server didn't responded to the connect request !!"+'\033[0m')
        print('\033[91m'+"\t>> Check the IP whitelisted addresses on which the DB is active"+'\033[0m')
        # print('\033[93m'+e+'\033[0m')
        sys.exit()
    try:
        from neo4jDBC import Neo4jDBC
        mini_batch = mongoDBC_obj.findMany() # get batch of 5 docs
        doc_names = []
        for doc in mini_batch:
            Neo4jDBC().insertEntities(doc['doc_name'], doc['entity_list'])
            # Neo4jDBC().printAllNodes()
            doc_names.append(doc['doc_name'])
        mongoDBC_obj.deleteMany(doc_names)  # delete batch from mongoDB
    except Exception as e:
        print('\033[91m'+"\n[ERR] Neo4j DB didn't responded to the connect request !!"+'\033[0m')
        print('\033[91m'+"\t>> Check the port number on which the DB is active"+'\033[0m')
        # print('\033[93m'+e+'\033[0m')
        sys.exit()


if __name__ == "__main__":
    test_data = [{
        "doc_name" : "Albert einstein",
        "wiki_url" : "http://en.wikipedia.org/wiki/Albert_Einstein",
        "done" : True,
        "entity_list" : [
            {
                "subject": "Albert einstein",
                "relation": "published",
                "object": "300 scientific papers",
                "subj_type": "ORG",
                "obj_type": "NOUN_CHUNK"
            }
        ]
    }]
    try:
        mongoDBC_obj = MongoDBC()
    except Exception as e:
        print('\033[91m'+"\n[ERR] MongoDB Atlas server didn't responded to the connect request !!"+'\033[0m')
        print('\033[91m'+"\t>> Check the IP whitelisted addresses on which the DB is active"+'\033[0m')
        # print('\033[93m'+e+'\033[0m')
        sys.exit()

    # ---- DB ops ----
    mongoDBC_obj.insertMany(test_data)
    mongoDBC_obj.deleteMany(["Dhyey Thumar", "Albert-einstein"])
    # print(mongoDBC_obj.findOne("Albert einstein"))
    # for doc in mongoDBC_obj.findMany():
    #     print(doc['doc_name'])
    mongoDBC_obj.totalDocCount()
